# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mahdi/projects/drsignal/drsignal-server-lib/src/lib/service/service.py
# Compiled at: 2020-03-28 10:28:10
# Size of source mod 2**32: 945 bytes
import functools, inspect

def action(name):

    def decorator(function):

        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            return function(*args, **kwargs)

        wrapper.action_info = {'name':name, 
         'handler':wrapper}
        return wrapper

    return decorator


class ActionError(Exception):

    def __init__(self, status, message):
        self.info = {'status':status, 
         'message':message}
        super().__init__(message)


class Service:

    def __init__(self):
        self.action_infos = self._detect_actions()

    def _detect_actions(self):
        all_methods = inspect.getmembers(self, predicate=(inspect.ismethod))
        action_infos = []
        for method in all_methods:
            if hasattr(method[1], 'action_info'):
                action_infos.append(method[1].action_info)

        return action_infos