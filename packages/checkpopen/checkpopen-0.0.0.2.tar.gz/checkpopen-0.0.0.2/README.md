[![PyPI](https://img.shields.io/pypi/v/checkpopen)](https://pypi.org/project/checkpopen/)

## CheckPopen

Popen context manager variant that raises CalledProcessError like check\_call.

1. Context manager is not available in Python2.
2. When exceptions happened in Python3 original context, the process might get stuck especially when the process is daemon.
   We try to kill the process implicitly when exception happens.
3. Not closing stdin/stdout implicitly to make sure we communicate with the pipe correctly.
