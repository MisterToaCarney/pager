import asyncio
import zmq
import zmq.asyncio
import pmt
import bitstring
import bchlib

# POCSAG Protocol ref
# https://www.raveon.com/pdfiles/AN142(POCSAG).pdf

ctx = zmq.asyncio.Context()
# bch = bchlib.BCH(0b10000000011011, 2)
bch = bchlib.BCH(1897, 1)

async def read_socket():
    with ctx.socket(zmq.SUB) as s:
        s.setsockopt(zmq.SUBSCRIBE, b"")
        s.connect("ipc:///tmp/pager_pdu1.socket")
        while True:
            message_bytes, = await s.recv_multipart()
            header, payload = decode_polymorhic_type(message_bytes)

            print("Header:", header)
            print("Payload:", payload)

            decode_batch(payload)

            print()

def decode_polymorhic_type(message_bytes):
    pdu = pmt.deserialize_str(message_bytes)
    if not pmt.is_pair(pdu): return None

    header = pmt.to_python(pmt.car(pdu))
    payload = pmt.to_python(pmt.cdr(pdu))

    payload = payload.tobytes()

    return header, payload

def decode_batch(batch: bytes):
    for i in range(16):
        frame_number = i // 2
        codeword_bytes = batch[i*4 : (i+1)*4]
        codeword = bitstring.BitArray(codeword_bytes)
        is_idle_word = codeword.hex == '7a89c197'
        if is_idle_word:
            continue

        pass
        is_parity_valid = codeword.bin.count("1") % 2 == 0
        encoded, parity_bit = codeword.unpack("uint:31, bool:1")




if __name__ == "__main__":
    asyncio.run(read_socket())