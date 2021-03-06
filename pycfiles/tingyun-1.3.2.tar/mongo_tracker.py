# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nb/publish/btw/tingyun/tingyun/armoury/ammunition/mongo_tracker.py
# Compiled at: 2016-06-30 06:13:10
"""this module used to wrap the specify armory to trace

"""
import logging
from tingyun.armoury.ammunition.timer import Timer
from tingyun.armoury.ammunition.tracker import current_tracker
from tingyun.logistics.warehouse.mongo_node import MongoNode
from tingyun.logistics.basic_wrapper import wrap_object, FunctionWrapper
console = logging.getLogger(__name__)

class MongoTracker(Timer):
    """
    """

    def __init__(self, tracker, schema, method):
        """
        :return:
        """
        super(MongoTracker, self).__init__(tracker)
        self.method = method
        self.schema = schema

    def create_node(self):
        """
        :return:
        """
        tracker = current_tracker()
        if tracker:
            tracker.mongo_time = self.duration
        return MongoNode(method=self.method, children=self.children, start_time=self.start_time, schema=self.schema, end_time=self.end_time, duration=self.duration, exclusive=self.exclusive)

    def terminal_node(self):
        return True


def mongo_trace_wrapper(wrapped, schema, method):
    """
    :return:
    """

    def dynamic_wrapper(wrapped, instance, args, kwargs):
        tracker = current_tracker()
        if tracker is None:
            return wrapped(*args, **kwargs)
        else:
            _method = method
            if callable(method):
                if instance is not None:
                    _method = method(instance, *args, **kwargs)
                else:
                    _method = method(*args, **kwargs)
            _schema = schema
            if callable(schema):
                if instance is not None:
                    _schema = schema(instance, *args, **kwargs)
                else:
                    _schema = schema(*args, **kwargs)
            with MongoTracker(tracker, _schema, _method):
                return wrapped(*args, **kwargs)
            return

    def literal_wrapper(wrapped, instance, args, kwargs):
        tracker = current_tracker()
        if tracker is None:
            return wrapped(*args, **kwargs)
        else:
            with MongoTracker(tracker, method):
                return wrapped(*args, **kwargs)
            return

    if callable(method) or callable(schema):
        return FunctionWrapper(wrapped, dynamic_wrapper)
    return FunctionWrapper(wrapped, literal_wrapper)


def wrap_mongo_trace(module, object_path, schema, method):
    wrap_object(module, object_path, mongo_trace_wrapper, (schema, method))