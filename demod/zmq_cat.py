import zmq
import sys

ctx = zmq.Context()

with ctx.socket(zmq.SUB) as s:
    s.setsockopt(zmq.SUBSCRIBE, b"")
    s.connect(f"ipc:///tmp/pager_{sys.argv[1]}.socket")
    while True:
        msg_bytes, = s.recv_multipart()
        sys.stdout.buffer.write(msg_bytes)
