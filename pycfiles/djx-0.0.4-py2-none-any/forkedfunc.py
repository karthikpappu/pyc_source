# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-zr3xXj/py/py/_process/forkedfunc.py
# Compiled at: 2019-02-14 00:35:48
"""
    ForkedFunc provides a way to run a function in a forked process
    and get at its return value, stdout and stderr output as well
    as signals and exitstatusus.
"""
import py, os, sys, marshal

def get_unbuffered_io(fd, filename):
    f = open(str(filename), 'w')
    if fd != f.fileno():
        os.dup2(f.fileno(), fd)

    class AutoFlush:

        def write(self, data):
            f.write(data)
            f.flush()

        def __getattr__(self, name):
            return getattr(f, name)

    return AutoFlush()


class ForkedFunc:
    EXITSTATUS_EXCEPTION = 3

    def __init__(self, fun, args=None, kwargs=None, nice_level=0, child_on_start=None, child_on_exit=None):
        if args is None:
            args = []
        if kwargs is None:
            kwargs = {}
        self.fun = fun
        self.args = args
        self.kwargs = kwargs
        self.tempdir = tempdir = py.path.local.mkdtemp()
        self.RETVAL = tempdir.ensure('retval')
        self.STDOUT = tempdir.ensure('stdout')
        self.STDERR = tempdir.ensure('stderr')
        pid = os.fork()
        if pid:
            self.pid = pid
        else:
            self.pid = None
            self._child(nice_level, child_on_start, child_on_exit)
        return

    def _child(self, nice_level, child_on_start, child_on_exit):
        sys.stdout = stdout = get_unbuffered_io(1, self.STDOUT)
        sys.stderr = stderr = get_unbuffered_io(2, self.STDERR)
        retvalf = self.RETVAL.open('wb')
        EXITSTATUS = 0
        try:
            if nice_level:
                os.nice(nice_level)
            try:
                if child_on_start is not None:
                    child_on_start()
                retval = self.fun(*self.args, **self.kwargs)
                retvalf.write(marshal.dumps(retval))
                if child_on_exit is not None:
                    child_on_exit()
            except:
                excinfo = py.code.ExceptionInfo()
                stderr.write(str(excinfo._getreprcrash()))
                EXITSTATUS = self.EXITSTATUS_EXCEPTION

        finally:
            stdout.close()
            stderr.close()
            retvalf.close()

        os.close(1)
        os.close(2)
        os._exit(EXITSTATUS)
        return

    def waitfinish(self, waiter=os.waitpid):
        pid, systemstatus = waiter(self.pid, 0)
        if systemstatus:
            if os.WIFSIGNALED(systemstatus):
                exitstatus = os.WTERMSIG(systemstatus) + 128
            else:
                exitstatus = os.WEXITSTATUS(systemstatus)
        else:
            exitstatus = 0
        signal = systemstatus & 127
        if not exitstatus and not signal:
            retval = self.RETVAL.open('rb')
            try:
                retval_data = retval.read()
            finally:
                retval.close()

            retval = marshal.loads(retval_data)
        else:
            retval = None
        stdout = self.STDOUT.read()
        stderr = self.STDERR.read()
        self._removetemp()
        return Result(exitstatus, signal, retval, stdout, stderr)

    def _removetemp(self):
        if self.tempdir.check():
            self.tempdir.remove()

    def __del__(self):
        if self.pid is not None:
            self._removetemp()
        return


class Result(object):

    def __init__(self, exitstatus, signal, retval, stdout, stderr):
        self.exitstatus = exitstatus
        self.signal = signal
        self.retval = retval
        self.out = stdout
        self.err = stderr