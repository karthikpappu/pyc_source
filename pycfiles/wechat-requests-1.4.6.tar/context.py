# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: f:\pipeline\wechat\src\wechat\message\context.py
# Compiled at: 2018-05-16 13:00:23
from six import iteritems

class Context(dict):

    def __init__(self, **kwargs):
        dict.__init__(self, kwargs)

    @property
    def message(self):
        return self.get('message', None)

    @property
    def raw_message(self):
        return self.get('raw_message', None)

    @property
    def handler(self):
        return self.get('handler', None)

    @property
    def handle_result(self):
        return self.get('handle_result', None)

    @property
    def should_continue(self):
        return self.get('should_continue', False)

    def set(self, key, val):
        return self.__setitem__(key, val)

    def defaults(self, **kwargs):
        for k, v in iteritems(kwargs):
            if k not in self:
                self.set(k, v)

        return self

    def extends(self, **kwargs):
        self.update(kwargs)
        return self

    @classmethod
    def new(cls, **kwargs):
        return cls(**kwargs)