# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.6.7/lib/python3.6/site-packages/satella/instrumentation/memory/memthread.py
# Compiled at: 2020-04-14 13:42:23
# Size of source mod 2**32: 7670 bytes
import logging, os, time, typing as tp, psutil
from satella.coding.concurrent import CallableGroup
from satella.coding.concurrent import TerminableThread
from satella.coding.structures import Singleton
from satella.time import measure
from .conditions import BaseCondition, ZerothSeverity
logger = logging.getLogger(__name__)
__all__ = [
 'MemoryPressureManager']

class CallNoMoreOftenThan:
    __slots__ = ('interval', 'callable', 'last_called')

    def __init__(self, interval: int, callable_: tp.Callable[([], None)]):
        self.interval = interval
        self.callable = callable_
        self.last_called = 0

    def __call__(self):
        if time.monotonic() - self.last_called >= self.interval:
            self.callable()
            self.last_called = time.monotonic()


@Singleton
class MemoryPressureManager(TerminableThread):
    __doc__ = "\n    Manager of the memory pressure.\n\n    The program is in some severity state. The baseline state is 0, meaning everything's OK.\n\n    Please note that it is sufficient to instantiate this class for the thread to run.\n\n    Eg.\n\n    >>> mt = MemoryPressureManager(maximum_available=4*GB, severity_levels=[80, 90])\n    >>> @mt.register_on_severity(1)\n    >>> def trigger_a():\n    >>>     print('80% consumption of memory exceeded')\n    >>> @mt.register_on_severity(2)\n    >>> def trigger_b():\n    >>>     print('90% consumption of memory exceeded')\n\n    :param maximum_available: maximum amount of memory that this program can use\n    :param severity_levels: this defines the levels of severity. A level is reached when program's\n        consumption is other this many percent of it's maximum_available amount of memory.\n    :param check_interval: amount of seconds of pause between consecutive checks\n    :param log_transitions: whether to log to logger when a transition takes place\n    "
    __slots__ = ('process', 'maximum_available', 'severity_levels', 'callbacks_on_entered',
                 'callbacks_on_remains', 'current_severity_level', 'check_interval',
                 'log_transitions')

    def __init__(self, maximum_available=None, severity_levels=None, check_interval=10, log_transitions=True):
        super().__init__(daemon=True)
        self.log_transitions = log_transitions
        self.process = psutil.Process(os.getpid())
        self.maximum_available = maximum_available
        self.severity_levels = [ZerothSeverity()] + (severity_levels or [])
        self.callbacks_on_entered = [CallableGroup(gather=False) for _ in range(len(self.severity_levels))]
        self.callbacks_on_remains = [CallableGroup(gather=False) for _ in range(len(self.severity_levels))]
        self.callbacks_on_left = [CallableGroup(gather=False) for _ in range(len(self.severity_levels))]
        self.current_severity_level = 0
        self.stopped = False
        self.check_interval = check_interval
        self.start()

    def advance_to_severity_level(self, target_level: int):
        while self.current_severity_level != target_level:
            delta = target_level - self.current_severity_level
            delta = int(delta / abs(delta))
            if delta > 0:
                self.current_severity_level += delta
                self.callbacks_on_entered[self.current_severity_level]()
                if self.log_transitions:
                    logger.warning('Entered severity level %s' % (self.current_severity_level,))
            elif delta < 0:
                self.callbacks_on_left[self.current_severity_level]()
                if self.log_transitions:
                    logger.warning('Left severity level %s' % (self.current_severity_level,))
                self.current_severity_level += delta

    def stop(self):
        """Stop this thread from operating"""
        self.stopped = True

    def resume(self):
        """Resume the operation of this thread"""
        self.stopped = False

    def loop(self) -> None:
        if self.stopped:
            return time.sleep(self.check_interval)
        with measure() as (measurement):
            severity_level = self.calculate_severity_level()
            if self.current_severity_level != severity_level:
                self.advance_to_severity_level(severity_level)
            else:
                self.callbacks_on_remains[severity_level]()
        elapsed = measurement()
        if elapsed < self.check_interval:
            time.sleep(self.check_interval - elapsed)

    def calculate_severity_level(self) -> int:
        """
        This returns a severity level. 0 is the baseline severity level.
        """
        memory_info = self.process.memory_info()
        for level, condition in reversed(list(enumerate(self.severity_levels))):
            if condition.can_fire(memory_info, self.maximum_available):
                return level

    @staticmethod
    def register_on_entered_severity(severity: int):
        """
        Register this handler to fire on entered a particular severity level.

        This means that situation has gotten worse.

        Use like this:

        >>> MemoryPressureManager.register_on_entered_severity(1)
        >>> def entered_severity_one():
        >>>     print('Entered memory severity level 1')

        :param severity: severity level to react to
        """

        def outer(fun):
            MemoryPressureManager().callbacks_on_entered[severity].add(fun)
            return fun

        return outer

    @staticmethod
    def register_on_left_severity(severity: int):
        """
        Register a handler to be called when given severity level is left. This means
        that we have advanced to a lower severity level.

        >>> MemoryPressureManager.register_on_left_severity(1)
        >>> def entered_severity_one():
        >>>     print('Memory comsumption no longer 1')

        :param severity: severity level to leave
        """

        def outer(fun):
            MemoryPressureManager().callbacks_on_left[severity].add(fun)
            return fun

        return outer

    @staticmethod
    def register_on_remaining_in_severity(severity: int, call_no_more_often_than: int=0):
        """
        Register this handler to fire on remaining in a particular severity level. Use like this:

        >>> MemoryPressureManager.register_on_remaining_in_severity(0, 30)
        >>> def entered_severity_one():
        >>>     print('Memory comsumption OK. I am called no more often than each 30 seconds')

        :param severity: severity level
        :param call_no_more_often_than: call no more often than this amount of seconds
        """

        def outer(fun):
            MemoryPressureManager().callbacks_on_remains[severity].add(CallNoMoreOftenThan(call_no_more_often_than, fun))
            return fun

        return outer