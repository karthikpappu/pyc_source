# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/buzz/contents.py
# Compiled at: 2019-12-18 07:21:19
# Size of source mod 2**32: 2310 bytes
import re
from collections import MutableSequence
from .utils import _load_corpus

class Contents(MutableSequence):
    __doc__ = '\n    Holder for ordered collections of files or subcorpora\n    '

    def __init__(self, data=[], is_parsed=True, name=None):
        self.list = data
        self.is_parsed = is_parsed
        self.name = name

    def __repr__(self):
        return str(self.list)

    def __len__(self):
        return len(self.list)

    def __bool__(self):
        if self.list:
            return True
        return False

    def _try_to_get_same(self, name):
        return next((i for i in self.list if i.name == name), None)

    def __getattr__(self, attr):
        """
        Attribute style access to subcorpora/files, preferring former
        """
        found = self._try_to_get_same(attr)
        if found:
            return found
        raise AttributeError(f"No such attribute: {attr}")

    def __getitem__(self, i):
        """
        dict style lookup of files
        """
        if isinstance(i, str):
            found = self._try_to_get_same(i)
            if found:
                return found
            raise KeyError(f"No such object: {i}")
        if isinstance(i, type(re.compile('x'))):
            return Contents([s for s in self.list if re.search(i, s.name)])
        if isinstance(i, slice):
            return Contents(self.list[i])
        return self.list[i]

    def __delitem__(self, i):
        del self.list[i]

    def __setitem__(self, i, v):
        self.list[i] = v

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError(f"Not same class: {self.__class__} vs {other.__class__}")
        if len(self) != len(other):
            return False
        return all((a == b for a, b in zip(self, other)))

    def insert(self, i, v):
        if self:
            if not isinstance(v, self[0].__class__):
                raise TypeError(f"Not same class: {self[0].__class__} vs {v.__class__}")
        self.list.insert(i, v)

    def load(self, **kwargs):
        """
        Load this data just as we do a Corpus
        """
        return _load_corpus(self, **kwargs)