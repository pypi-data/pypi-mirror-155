#!/usr/bin/env python
#coding:utf-8

import sys
import subprocess
import signal
import time
from contextlib import contextmanager

def StopProcs(procs, waitDuration=None):
    if waitDuration is None:
        waitDuration = 5
    for proc in procs:
        if proc.poll() is None:
            proc.send_signal(signal.SIGINT)
    for _ in range(int(waitDuration*100*0.8)):
        if all(proc.poll() is not None for proc in procs):
            return
        time.sleep(0.01)
    for proc in procs:
        if proc.poll() is None:
            proc.send_signal(signal.SIGTERM)
    for _ in range(int(waitDuration*100*0.2)):
        if all(proc.poll() is not None for proc in procs):
            return
        time.sleep(0.01)
    for proc in procs:
        if proc.poll() is None:
            proc.send_signal(signal.SIGKILL)
            proc.wait()

@contextmanager
def CheckPopen(args, **kwargs):
    '''
    context manager version of Popen.

    1. Context manager is not available in Python2.
    2. When exceptions happened in Python3 original context, the process might get stuck especially when the process is daemon.
       We try to kill the process implicitly when exception happens.
    3. Not closing stdin/stdout implicitly to make sure we communicate with the pipe correctly.
    '''

    waitDuration = kwargs.pop('waitDuration', None)
    proc = subprocess.Popen(args, **kwargs)
    exc_type = None
    try:
        yield proc
    except Exception:
        exc_type = sys.exc_info()[0]
        raise
    finally:
        if exc_type is not None:
            StopProcs([proc], waitDuration=waitDuration)
        elif proc.wait():
            raise subprocess.CalledProcessError(proc.returncode, args)
