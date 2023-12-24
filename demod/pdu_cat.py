import zmq
import zmq.asyncio
import sys
import asyncio
import pmt
import numpy as np
import bitstring
from pyfinite import ffield

ctx = zmq.asyncio.Context()

F = ffield.FField(31)
G = ffield.FElement(F, 0b11101101001) # generator polynomial

buffer = bitstring.BitArray()

async def read_socket():
    with ctx.socket(zmq.SUB) as s:
        s.setsockopt(zmq.SUBSCRIBE, b"")
        # s.connect(f"ipc:///tmp/pager_{sys.argv[1]}.socket")
        s.connect("ipc:///tmp/pager_pdu1.socket")
        while True:
            msg_bytes, = await s.recv_multipart()
            await process(msg_bytes)

async def process(message):
    pdu = pmt.deserialize_str(message)
    if not pmt.is_pair(pdu): return None
    
    header = pmt.to_python(pmt.car(pdu))
    payload = pmt.to_python(pmt.cdr(pdu))
    # print(header)

    payload = payload.tobytes()

    decode(payload)
    
    # print("----")

def decode(batch):
    global buffer
    for i in range(16):
        frame_number = i // 2
        codeword = batch[i*4:(i+1)*4]
        s = bitstring.BitArray(codeword)
        is_idle_word = s.hex == '7a89c197'
        if is_idle_word:
            readout_buffer()
            continue

        # ECC
        is_parity_valid = s.bin.count("1") % 2 == 0
        encoded, parity_bit = s.unpack("uint:31, bool:1")
        encoded = ffield.FElement(F, encoded)
        is_bch_valid = encoded % G == 0

        if (not is_parity_valid) or (not is_bch_valid): 
            print("DROPPED", "Parity:", is_parity_valid, "BCH:", is_bch_valid)
            continue
            
        is_address_word = s[0] == False
        if is_address_word:
            readout_buffer()

            address_bits = s[1:19]
            function_bits = s[20:22]
            full_address = address_bits + bin(frame_number)
            full_address_alt = bin(frame_number) + address_bits
            print("A", full_address.uint, full_address_alt.uint)
            pass
        else:
            buffer += s[1:21]
        
        

        # if is_bch_valid: print("Y", end='')
        # else: print("*", end='')
        

        pass

def readout_buffer():
    global buffer
    if len(buffer) == 0: return

    output = b''

    num_chars = len(buffer) // 7
    for i in range(num_chars):
        start = i * 7
        end = (i + 1) * 7
        char_bits = bitstring.BitArray(buffer[start:end])
        char_bits.reverse()
        char = [0] + char_bits
        output += char.bytes

    print(output.decode('ascii'))

    buffer.clear()

# Function here for reference,
# not used as bits are packed at the PHY level
def pack_bits(payload):
    unpacked = payload.reshape(-1, 8)
    unpacked = unpacked << np.flip(np.arange(8))
    packed = unpacked.sum(1, dtype=np.uint8)
    return packed.tobytes()

if __name__ == "__main__": 
    asyncio.run(read_socket())


