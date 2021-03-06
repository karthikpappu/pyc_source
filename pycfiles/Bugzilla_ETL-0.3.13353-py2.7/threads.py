# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\bzETL\util\threads.py
# Compiled at: 2013-12-18 14:05:11
from datetime import datetime, timedelta
import threading, thread, time
from .struct import nvl
DEBUG = True

class Lock(object):
    """
    SIMPLE LOCK (ACTUALLY, A PYTHON threadind.Condition() WITH notify() BEFORE EVERY RELEASE)
    """

    def __init__(self, name=''):
        self.monitor = threading.Condition()
        self.name = name

    def __enter__(self):
        self.monitor.acquire()
        return self

    def __exit__(self, a, b, c):
        self.monitor.notify()
        self.monitor.release()

    def wait(self, timeout=None, till=None):
        if till:
            timeout = (datetime.utcnow() - till).total_seconds()
            if timeout < 0:
                return
        self.monitor.wait(timeout=timeout)

    def notify_all(self):
        self.monitor.notify_all()


class Queue(object):
    """
    SIMPLE MESSAGE QUEUE, multiprocessing.Queue REQUIRES SERIALIZATION, WHICH IS HARD TO USE JUST BETWEEN THREADS
    """

    def __init__(self, max=None):
        """
        max - LIMIT THE NUMBER IN THE QUEUE, IF TOO MANY add() AND extend() WILL BLOCK
        """
        self.max = nvl(max, 1073741824)
        self.keep_running = True
        self.lock = Lock('lock for queue')
        self.queue = []

    def __iter__(self):
        while self.keep_running:
            try:
                value = self.pop()
                if value != Thread.STOP:
                    yield value
            except Exception as e:
                from .logs import Log
                Log.warning('Tell me about what happened here', e)

    def add(self, value):
        with self.lock:
            if self.keep_running:
                self.queue.append(value)
            while self.keep_running and len(self.queue) > self.max:
                self.lock.wait()

        return self

    def extend(self, values):
        with self.lock:
            if self.keep_running:
                self.queue.extend(values)
            while self.keep_running and len(self.queue) > self.max:
                self.lock.wait()

    def __len__(self):
        with self.lock:
            return len(self.queue)

    def pop(self):
        with self.lock:
            while self.keep_running:
                if self.queue:
                    value = self.queue.pop(0)
                    if value == Thread.STOP:
                        self.keep_running = False
                    return value
                self.lock.wait()

            return Thread.STOP

    def pop_all(self):
        """
        NON-BLOCKING POP ALL IN QUEUE, IF ANY
        """
        with self.lock:
            if not self.keep_running:
                return [Thread.STOP]
            else:
                if not self.queue:
                    return []
                for v in self.queue:
                    if v == Thread.STOP:
                        self.keep_running = False

                output = list(self.queue)
                del self.queue[:]
                return output

    def close(self):
        with self.lock:
            self.keep_running = False


class AllThread(object):
    """
    RUN ALL ADDED FUNCTIONS IN PARALLEL, BE SURE TO HAVE JOINED BEFORE EXIT
    """

    def __init__(self):
        self.threads = []

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.join()

    def join(self):
        exceptions = []
        try:
            for t in self.threads:
                response = t.join()
                if 'exception' in response:
                    exceptions.append(response['exception'])

        except Exception as e:
            from .logs import Log
            Log.warning('Problem joining', e)

        if exceptions:
            from .logs import Log
            Log.error('Problem in child threads', exceptions)

    def add(self, target, *args, **kwargs):
        """
        target IS THE FUNCTION TO EXECUTE IN THE THREAD
        """
        t = Thread.run(target.__name__, target, *args, **kwargs)
        self.threads.append(t)


class Thread(object):
    """
    join() ENHANCED TO ALLOW CAPTURE OF CTRL-C, AND RETURN POSSIBLE THREAD EXCEPTIONS
    run() ENHANCED TO CAPTURE EXCEPTIONS
    """
    num_threads = 0
    STOP = 'stop'
    TIMEOUT = 'TIMEOUT'

    def __init__(self, name, target, *args, **kwargs):
        self.name = name
        self.target = target
        self.response = None
        self.synch_lock = Lock()
        self.args = args
        self.kwargs = kwargs.copy()
        self.kwargs['please_stop'] = self.kwargs.get('please_stop', Signal())
        self.please_stop = self.kwargs['please_stop']
        self.stopped = Signal()
        return

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        if isinstance(type, BaseException):
            self.please_stop.go()
        self.join()
        self.args = None
        self.kwargs = None
        return

    def start(self):
        try:
            self.thread = thread.start_new_thread(Thread._run, (self,))
        except Exception as e:
            from .logs import Log
            Log.error('Can not start thread', e)

    def stop(self):
        self.please_stop.go()

    def _run(self):
        try:
            try:
                if self.target is not None:
                    response = self.target(*self.args, **self.kwargs)
                    with self.synch_lock:
                        self.response = {'response': response}
            except Exception as e:
                with self.synch_lock:
                    self.response = {'exception': e}
                from .logs import Log
                Log.error('Problem in thread', e)

        finally:
            self.stopped.go()
            del self.target
            del self.args
            del self.kwargs

        return

    def is_alive(self):
        return not self.stopped

    def join(self, timeout=None, till=None):
        """
        RETURN THE RESULT OF THE THREAD EXECUTION (INCLUDING EXCEPTION)
        """
        if not till and timeout:
            till = datetime.utcnow() + timedelta(seconds=timeout)
        if till is None:
            while True:
                with self.synch_lock:
                    for i in range(10):
                        if self.stopped:
                            return self.response
                        self.synch_lock.wait(0.5)

                from .logs import Log
                if DEBUG:
                    Log.note('Waiting on thread {{thread}}', {'thread': self.name})

        else:
            self.stopped.wait_for_go(till=till)
            if self.stopped:
                return self.response
            from logs import Except
            raise Except(type=Thread.TIMEOUT)
        return

    @staticmethod
    def run(name, target, *args, **kwargs):
        if 'please_stop' not in target.__code__.co_varnames:
            from logs import Log
            Log.error('function must have please_stop argument for signalling emergency shutdown')
        Thread.num_threads += 1
        output = Thread(name, target, *args, **kwargs)
        output.start()
        return output

    @staticmethod
    def sleep(seconds=None, till=None):
        if seconds is not None:
            time.sleep(seconds)
        if till is not None:
            duration = (till - datetime.utcnow()).total_seconds()
            if duration > 0:
                time.sleep(duration)
        return


class Signal(object):
    """
    SINGLE-USE THREAD SAFE SIGNAL
    """

    def __init__(self):
        self.lock = Lock()
        self._go = False
        self.job_queue = []

    def __bool__(self):
        with self.lock:
            return self._go

    def __nonzero__(self):
        with self.lock:
            return self._go

    def wait_for_go(self, timeout=None, till=None):
        with self.lock:
            while not self._go:
                self.lock.wait(timeout=timeout, till=till)

            return True

    def go(self):
        with self.lock:
            if self._go:
                return
            self._go = True
            jobs = self.job_queue
            self.job_queue = []
            self.lock.notify_all()
        for j in jobs:
            j()

    def is_go(self):
        with self.lock:
            return self._go

    def on_go(self, target):
        """
        RUN target WHEN SIGNALED
        """
        with self.lock:
            if self._go:
                target()
            else:
                self.job_queue.append(target)


class ThreadedQueue(Queue):
    """
    TODO: Check that this queue is not dropping items at shutdown
    DISPATCH TO ANOTHER (SLOWER) queue IN BATCHES OF GIVEN size
    """

    def __init__(self, queue, size, max=None):
        if max == None:
            max = size * 2
        Queue.__init__(self, max=max)

        def size_pusher(please_stop):
            please_stop.on_go(lambda : self.add(Thread.STOP))
            from .queries import Q
            for i, g in Q.groupby(self, size=size):
                try:
                    queue.extend(g)
                    if please_stop:
                        from logs import Log
                        Log.warning('ThreadedQueue stopped early, with {{num}} items left in queue', {'num': len(self)})
                        return
                except Exception as e:
                    from logs import Log
                    Log.warning('Can not push data to given queue', e)

        self.thread = Thread.run('threaded queue', size_pusher)
        return

    def __enter__(self):
        return self

    def __exit__(self, a, b, c):
        self.add(Thread.STOP)
        if isinstance(b, BaseException):
            self.thread.please_stop.go()
        self.thread.join()