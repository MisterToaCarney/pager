import zmq
import zmq.asyncio
import sys
import asyncio
import time

ctx = zmq.asyncio.Context()

pre_buffer_size = 8

async def read_socket(q: asyncio.Queue, buffer_ready: asyncio.Event):
    with ctx.socket(zmq.SUB) as s:
        s.setsockopt(zmq.SUBSCRIBE, b"")
        s.connect(f"ipc:///tmp/pager_{sys.argv[1]}.socket")
        while True:
            msg_bytes, = await s.recv_multipart()
            await q.put(msg_bytes)
            if q.qsize() > pre_buffer_size: buffer_ready.set()
            
async def write_stdout(q: asyncio.Queue, buffer_ready: asyncio.Event):
    await buffer_ready.wait()
    while True:
        sys.stdout.buffer.write(await q.get())

async def main():
    buffer_ready = asyncio.Event()
    q = asyncio.Queue()
    await asyncio.gather(read_socket(q, buffer_ready), write_stdout(q, buffer_ready))

if __name__ == "__main__": asyncio.run(main())
