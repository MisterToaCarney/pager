import zmq
import time
import sys
import subprocess

command = ["multimon-ng", "-c", "-a", "POCSAG512", "-a", "POCSAG1200", "-a", "POCSAG2400", "-a", "FLEX", "-"]

with zmq.Context() as ctx:
    with ctx.socket(zmq.SUB) as s:
        s.setsockopt(zmq.SUBSCRIBE, b"")
        s.connect(f"ipc:///tmp/pager_{sys.argv[1]}.socket")

        with subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE) as p1:
            while True:
                msg_bytes, = s.recv_multipart()
                #p1.stdin.write(msg_bytes)
                out = p1.stdout.read()
                print(out)
                