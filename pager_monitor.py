from multiprocessing import Process, Event

def dsp_process(exit_event):
    from grc import pager
    pager.main()
    exit_event.set()

def demod_process(exit_event):
    from demod import demod
    exit_event.set()

if __name__ == "__main__":
    exit_event = Event()

    dsp = Process(target=dsp_process, args=(exit_event,), daemon=True)
    demod = Process(target=demod_process, args=(exit_event,), daemon=True)
    dsp.start()
    demod.start()
    
    exit_event.wait()