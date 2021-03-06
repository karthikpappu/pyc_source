# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\srllib\process.py
# Compiled at: 2012-05-11 12:09:02
""" Functionality for managing child processes. """
from __future__ import absolute_import
import os.path, struct, cPickle, sys, signal, traceback, subprocess, errno, stat, time
from srllib import threading, util
from srllib._common import *
from srllib.error import BusyError, SrlError
from srllib.signal import Signal

class ChildError(SrlError):
    """ Exception detected in child process.
    
    If the original exception derives from L{PickleableException}, it is
    preserved, along with the traceback.
    @ivar orig_exception: The original exception, possibly C{None}.
    @ivar orig_traceback: Traceback of original exception, possibly C{None}.
    """

    def __init__(self, process_error):
        SrlError.__init__(self, 'Error in child process')
        if process_error.exc_class is not None:
            assert process_error.exc_message is not None
            assert process_error.exc_traceback is not None
            assert process_error.exc_arguments is not None
            self.orig_exception = process_error.exc_class(*process_error.exc_arguments)
        else:
            self.orig_exception = None
        self.orig_traceback = process_error.exc_traceback
        return


class PickleableException(SrlError):

    def __init__(self, msg, *args):
        SrlError.__init__(self, msg)
        self.arguments = (msg,) + args


class _ProcessError(object):
    """ Encapsulation of a child process error.
    
    Exceptions don't pickle in the standard fashion, so we do it like this.
    @ivar message: Error message.
    @ivar exc_message: Original exception message.
    @ivar exc_class: Class of original exception.
    @ivar exc_arguments: Arguments of original exception.
    @ivar exc_traceback: Traceback of original exception.
    """

    def __init__(self, msg, original_exc=None, original_tb=None):
        self.message = msg
        if original_exc is not None:
            self.exc_message = str(original_exc)
        else:
            self.exc_message = None
        if isinstance(original_exc, PickleableException):
            self.exc_class = original_exc.__class__
            self.exc_arguments = original_exc.arguments
        else:
            self.exc_class = None
            self.exc_arguments = None
        if original_tb is not None:
            self.exc_traceback = traceback.format_tb(original_tb)
        else:
            self.exc_traceback = None
        return


class PickleError(SrlError):
    pass


class _MthdProxy(object):

    def __init__(self, mthd):
        self.__obj, self.__cls, self.__name = mthd.im_self, mthd.im_class, mthd.im_func.func_name

    def __call__(self, *args, **kwds):
        name = self.__name
        if name.startswith('__'):
            name = '_%s%s' % (self.__cls.__name__, name)
        func = getattr(self.__cls, name)
        func(self.__obj, *args, **kwds)


class ChildDied(SrlError):
    """ Child died unexpectedly.
    @ivar exitcode: Child's exit code.
    @ivar stderr: Child's stderr.
    """

    def __init__(self, exitcode, stderr):
        SrlError.__init__(self, 'Child died unexpectedly (exit code %d)' % exitcode)
        self.exitcode, self.stderrr = exitcode, stderr


def terminate(process):
    """ Terminate a process of either the L{Process} type or the standard
    subprocess.Popen type.
    
    This method will block until it is determined that the process has in fact
    terminated.
    @note: On Windows, pywin32 is required.
    @return: The process's exit status.
    """
    r = process.poll()
    if r is not None:
        return r
    else:
        if get_os_name() == Os_Windows:
            import win32process, win32api
            handle = win32api.OpenProcess(1048577, False, process.pid)
            win32process.TerminateProcess(handle, -signal.SIGTERM)
        else:
            try:
                os.kill(process.pid, signal.SIGTERM)
                time.sleep(0.05)
            except OSError as err:
                if err.errno == errno.ECHILD:
                    pass
                else:
                    raise

        if process.poll() is None:
            os.kill(process.pid, signal.SIGKILL)
        return process.wait()


class Process(object):
    """ Invoke a callable in a child process.

    Instantiating an object of this class will spawn a child process, I{in which a
    provided callable is invoked}. Pipes are provided for the standard streams
    and a separate pipe for communication between parent and child. stdout and
    stderr are made non-blocking so they can easily be drained of data.
    @ivar stdout: Child's stdout file.
    @ivar stderr: Child's stderr file..
    """

    def __init__(self, child_func, child_args=[], child_kwds={}):
        """
        @param child_func: Function to be called in child process.
        @param child_args: Optional arguments for the child function.
        @param child_kwds: Optional keywords for the child function.
        @raise ChildDied: Child died unexpectedly.
        """
        self.__exit_rslt = None
        script_fname = self.__script_fname = util.create_tempfile(content='import cPickle, sys, struct\npipe_path = sys.argv[1]\nlnth = struct.unpack("@I", sys.stdin.read(4))[0]\nsys.path = cPickle.loads(sys.stdin.read(lnth))\nlnth = struct.unpack("@I", sys.stdin.read(4))[0]\nfunc, args, kwds = cPickle.loads(sys.stdin.read(lnth))\ntry: func(*args, **kwds)\nexcept Exception, err:\n    from srllib.process import _ProcessError\n    pickle = cPickle.dumps(_ProcessError("Error in child", err, sys.exc_info()[2]))\n    f = file(pipe_path, "wb")\n    try: f.write(pickle)\n    finally: f.close()\n')
        pipe_path = self.__errpipe_path = util.create_tempfile()
        prcs = self.__prcs = subprocess.Popen(['python', script_fname, pipe_path], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, bufsize=-1)
        import types
        if isinstance(child_func, types.MethodType):
            child_func = _MthdProxy(child_func)
        path_data = cPickle.dumps(sys.path)
        try:
            func_data = cPickle.dumps((child_func, child_args, child_kwds))
        except TypeError as err:
            print err
            raise PickleError('Failed to pickle %r, is this e.g. a nested definition?' % child_func)

        try:
            prcs.stdin.write(struct.pack('@I', len(path_data)))
            prcs.stdin.write(path_data)
            prcs.stdin.write(struct.pack('@I', len(func_data)))
            prcs.stdin.write(func_data)
            prcs.stdin.flush()
        except EnvironmentError as err:
            if err.errno == errno.EPIPE:
                exitcode = self.wait()
                raise ChildDied(exitcode, prcs.stderr.read())
            raise

        self._pid = prcs.pid
        return

    def __str__(self):
        return self.name

    @property
    def pid(self):
        return self._pid

    @property
    def stdout(self):
        return self.__prcs.stdout

    @property
    def stderr(self):
        return self.__prcs.stderr

    def close(self):
        """ Release resources.

        If the process is still alive, it is waited for.
        """
        if self.__exit_rslt is None:
            self.wait()
        os.remove(self.__errpipe_path)
        os.remove(self.__script_fname)
        return

    def poll(self):
        """ Check if child has exited.
        @return: If child has exited, its exit code, else C{None}.
        """
        rslt = self.__exit_rslt
        if rslt is not None:
            if isinstance(rslt, ChildError):
                raise rslt
            assert isinstance(rslt, int)
            return rslt
        r = self.__prcs.poll()
        f = file(self.__errpipe_path, 'rb')
        try:
            data = f.read()
        finally:
            f.close()

        if data:
            err = cPickle.loads(data)
            self.__exit_rslt = ChildError(err)
            raise self.__exit_rslt
        return r

    def wait(self):
        """ Wait for child to finish.
        @return: Child's exit code.
        @raise ChildError: Exception detected in child.
        """
        self.__prcs.wait()
        return self.poll()

    def terminate(self):
        """ Kill child process.
        
        Implemented using L{terminate}.
        """
        return terminate(self)

    def write_message(self, message, wait=True):
        """ Write message to other process.
        
        If this is the child process, message will be available for parent
        process and vice versa. This method may wait for the other process to
        "pick up the phone". A broken connection will result in EofError.
        @param message: An arbitrary object.
        @param wait: Wait for acknowledgement.
        """
        msg = cPickle.dumps(message)
        self.pipe_out.write(struct.pack('i', len(msg)))
        self.pipe_out.write(msg)
        if not wait:
            return
        a = self.pipe_in.read(1)
        if a == '':
            raise EofError

    def read_message(self):
        """ Read message from other process.
        
        If this is the child process, message will be read from parent process
        and vice versa. This method will wait until a message is actually
        received.
        @return: An arbitrary object written by the other process
        @raise EofError: Broken connection.
        """

        def read_data(lnth):
            data = self.pipe_in.read(lnth)
            if len(data) < lnth:
                raise EofError
            return data

        data = read_data(struct.calcsize('i'))
        msgLnth = struct.unpack('i', data)[0]
        data = read_data(msgLnth)
        try:
            self.pipe_out.write('a')
        except IOError:
            pass

        import cPickle
        obj = cPickle.loads(data)
        return obj

    def _poll(self, wait=False):
        if self._childRet is not None:
            return self._childRet
        else:
            if wait:
                flag = 0
            else:
                flag = os.WNOHANG
            while True:
                try:
                    pid, status = os.waitpid(self._pid, flag)
                except OSError as err:
                    if err.errno == errno.EINTR:
                        continue
                    raise

                break

            if pid != self._pid:
                return
            if os.WIFSIGNALED(status):
                self._childRet = -os.WTERMSIG(status)
            else:
                self._childRet = os.WEXITSTATUS(status)
            if self._childRet != 0:
                try:
                    obj = self.read_message()
                except EofError:
                    pass
                else:
                    if isinstance(obj, _ProcessError):
                        raise ChildError(obj)
            return self._childRet


class EofError(IOError):
    pass


class ThreadedProcessMonitor(object):
    """ Monitor a child process in a background thread.
    @group Signals: sig*
    @ivar process: The L{child process<Process>}
    @ivar sig_stdout: Triggered to deliver stdout output from the child process.
    @ivar sig_stderr: Triggered to deliver stderr output from the child process-
    @ivar sig_finished: Signal that monitor has finished, from background thread.
    Parameters: None.
    @ivar sig_failed: Signal that monitored process failed, from background
    thread. Paramaters: The caught exception.
    """

    def __init__(self, daemon=False, use_pty=False, pass_process=True):
        """
        @param daemon: Start background threads in daemon mode
        @param use_pty: Open pseudo-terminal for child process.
        @param pass_process: When executing functions in child processes,
        should the L{Process} object be passed as a parameter?
        """
        self.sig_stdout, self.sig_stderr, self.sig_finished, self.sig_failed = (
         Signal(), Signal(), Signal(), Signal())
        self.__process = None
        i, o = os.pipe()
        self._event_pipe_in, self._event_pipe_out = os.fdopen(i, 'r', 0), os.fdopen(o, 'w', 0)
        self._daemon = daemon
        self._thrd = None
        return

    @property
    def process(self):
        """ The monitored process. """
        return self.__process

    def __call__(self, child_func, child_args=[], child_kwds={}):
        """ Execute function in child process, monitored in background thread.
        @param child_func: Function to execute
        @param child_args: Arguments for child function
        @param child_kwds: Keywords for child function
        @raise BusyError: Already busy with a child process.
        """
        if self.__process is not None:
            raise BusyError('Another process is already being monitored')
        self.__exit_code = None
        self.__process = Process(child_func, child_args=child_args, child_kwds=child_kwds)
        thrd = self._thrd = threading.Thread(target=self._thrdfunc, daemon=self._daemon)
        thrd.start()
        return

    def monitor_command(self, arguments, cwd=None, env=None):
        """ Monitor a command.

        @return: The associated L{process<subprocess.Popen>}.
        """
        if self.__process is not None:
            raise BusyError('Another process is already being monitored')
        prcs = self.__process = subprocess.Popen(arguments, cwd=cwd, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        thrd = self._thrd = threading.Thread(target=self._thrdfunc, daemon=self._daemon)
        thrd.start()
        return prcs

    def wait(self):
        """ Wait for monitoring thread to finish.
        @return: The child process exit code. If the child raised a L{ChildError},
        this will be None.
        """
        if self._thrd is not None:
            self._thrd.join()
        return self.__exit_code

    def _thrdfunc(self):
        prcs = self.__process
        try:
            self.__exit_code = prcs.wait()
        except ChildError as err:
            self.sig_failed(err)
        else:
            self.sig_finished()

        if hasattr(prcs, 'close'):
            prcs.close()
        self.__process = None
        return