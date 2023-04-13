#!/usr/bin/env python3

from multiprocessing import Process, Event
import argparse

def dsp_process(exit_event, no_gui: bool = False):
    if no_gui: from grc import pager_nogui as pager
    else: from grc import pager
    pager.main()
    exit_event.set()

def demod_process(exit_event):
    from demod import demod
    exit_event.set()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--nogui", action="store_true", help="Run without QT user interface")
    args = parser.parse_args()

    exit_event = Event()

    dsp = Process(target=dsp_process, args=(exit_event, args.nogui), daemon=True)
    demod = Process(target=demod_process, args=(exit_event,), daemon=True)
    dsp.start()
    demod.start()
    
    exit_event.wait()