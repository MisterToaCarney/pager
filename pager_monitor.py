#!/usr/bin/env python3

from multiprocessing import Process, Event
import argparse

from demod import demod as d
from grc import pager_nogui, pager

def dsp_process(exit_event, no_gui: bool = False):
    try:
        print("Starting dsp")
        if no_gui: pager_nogui.main()
        else: pager.main()
        print("Ended dsp")
    finally:
        exit_event.set()

def demod_process(exit_event):
    try:
        print("Starting demod")
        d.start()
        print("Ended demod")
    finally:
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