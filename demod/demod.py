import asyncio
import zmq
import zmq.asyncio
import sys
import typing

ctx = zmq.asyncio.Context()
channels = ["ch1", "ch2"]

async def watch_stdout(proc: asyncio.subprocess.Process, log_file: typing.BinaryIO):
    while not proc.stdout.at_eof():
        mon_out = await proc.stdout.readline()
        sys.stdout.buffer.write(mon_out)
        log_file.write(mon_out)
        sys.stdout.buffer.flush()
        log_file.flush()

async def stream_stdin(proc: asyncio.subprocess.Process, q: asyncio.Queue):
    while proc.returncode is None:
        proc.stdin.write(await q.get())
        await proc.stdin.drain()

async def watch_zmq(channel: str, q: asyncio.Queue):
    with ctx.socket(zmq.SUB) as s:
        s.setsockopt(zmq.SUBSCRIBE, b"")
        s.connect(f"ipc:///tmp/pager_{channel}.socket")
        while True:
            msg_bytes, = await s.recv_multipart()
            await q.put(msg_bytes)

async def run_multimon(label: str = "ch0"):
    proc = await asyncio.create_subprocess_exec(
        "multimon-ng", "--label", label, "--timestamp", "-c", "-a", "POCSAG512", "-a", "POCSAG1200", "-a", "POCSAG2400", "-a", "FLEX", "-",
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE
    )
    return proc
        
async def run():
    procs = []
    q = []
    zmq_tasks = []
    in_tasks = []
    out_tasks = []

    log_file = open("pager.log", "ba")

    for channel in channels:
        new_proc = await run_multimon(label=channel)
        new_q = asyncio.Queue(128)

        procs.append(new_proc)
        q.append(new_q)
        
        zmq_tasks.append(asyncio.create_task(watch_zmq(channel, new_q)))
        in_tasks.append(asyncio.create_task(stream_stdin(new_proc, new_q)))
        out_tasks.append(asyncio.create_task(watch_stdout(new_proc, log_file)))

    await asyncio.gather(*[proc.wait() for proc in procs])

    log_file.close()


asyncio.run(run())