# This test requires Unix.

import sys
import os
import time
import signal
import pytest
from threading import Thread

mydir = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(mydir,'..'))
os.chdir(mydir)

from checkpopen import CheckPopen
from checkpopen import subprocess  # fear that subprocess impl might be different

def test_runs_on_true():
    with CheckPopen(['true'], shell=False, stdout=subprocess.PIPE) as proc:
        pass

def test_raises_on_false():
    with pytest.raises(subprocess.CalledProcessError):
        with CheckPopen(['false'], shell=False, stdout=subprocess.PIPE) as proc:
            pass

def test_stdout_is_expected():
    with CheckPopen(['pwd'], shell=False, stdout=subprocess.PIPE) as proc:
        assert proc.stdout.read().decode('utf-8').strip() == mydir

def test_small_communication():
    with CheckPopen(['cat'], shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE) as proc:
        # don't send larger than PAGE_SIZE, will get stuck. that's why proc.communicate is there
        proc.stdin.write('2048\n'.encode('utf-8'))
        proc.stdin.close()
        assert proc.stdout.read().decode('utf-8').strip() == '2048'

def test_exception():
    with pytest.raises(RuntimeError):
        # what should be better "daemon" to test this?
        with CheckPopen(['ssh', '-o', 'StrictHostKeyChecking=no', '-o', 'UserKnownHostsFile=/dev/null', '-N', 'localhost'], shell=False, stdin=subprocess.PIPE) as proc:
            raise RuntimeError('foobar')

def test_failsTo_raise_on_false():
    sys.version_info[0]<3 and pytest.xfail('cannot perform negative test on Py2')
    with subprocess.Popen(['false'], shell=False, stdout=subprocess.PIPE) as proc:
        pass

class TestFailsToRaiseException(object):

    def handler(self, sig, frame):
        raise RuntimeError('alarmed')

    @pytest.mark.parametrize('klass, expectedMessage', [
        (subprocess.Popen, 'alarmed'),
        (CheckPopen, 'exception during processing daemon'),
    ])
    def test_perform(self, klass, expectedMessage):
        if klass is subprocess.Popen:
            sys.version_info[0]<3 and pytest.xfail('cannot perform negative test on Py2')
        message = None
        try:
            # SIGALRM technique provided by pytest_timeout.py
            signal.signal(signal.SIGALRM, self.handler)
            signal.setitimer(signal.ITIMER_REAL, 5)
            with klass(['ssh', '-o', 'StrictHostKeyChecking=no', '-o', 'UserKnownHostsFile=/dev/null', '-N', 'localhost'], shell=False, stdin=subprocess.PIPE) as proc:
                raise RuntimeError('exception during processing daemon')
        except Exception as e:
            message = str(e)
        finally:
            signal.setitimer(signal.ITIMER_REAL, 0)
            signal.signal(signal.SIGALRM, signal.SIG_DFL)
            assert message == expectedMessage
