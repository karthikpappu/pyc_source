# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Toolserver/Context.py
# Compiled at: 2010-03-01 05:50:19
"""

Toolserver Framework for Python - Tool execution context class

Copyright (c) 2002, Georg Bauer <gb@rfc1437.de>

Permission is hereby granted, free of charge, to any person obtaining a copy of 
this software and associated documentation files (the "Software"), to deal in 
the Software without restriction, including without limitation the rights to 
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
 
the Software, and to permit persons to whom the Software is furnished to do so, 
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all 
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
 
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR 
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER 
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN 
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""
import copy, threading
from Toolserver.Config import config
from Toolserver.Utils import logInfo
_Namespace = {}
_Stacks = {}

class DynamicContext:

    def __nonzero__(self):
        return 1

    def __setattr__(self, key, value):
        current = threading.currentThread()
        if not _Namespace.has_key(current):
            _Namespace[current] = {}
        if len(key) == 0 or key[0] == '_':
            raise AttributeError(key)
        _Namespace[current][key] = value

    def __getattr__(self, key):
        current = threading.currentThread()
        if not _Namespace.has_key(current):
            _Namespace[current] = {}
        if _Namespace[current].has_key(key):
            return _Namespace[current][key]
        raise AttributeError(key)

    def __delattr__(self, key):
        current = threading.currentThread()
        if not _Namespace.has_key(current):
            _Namespace[current] = {}
        if _Namespace[current].has_key(key):
            del _Namespace[current][key]
        else:
            raise AttributeError(key)

    def _begin(self):
        current = threading.currentThread()
        logInfo('starting context in thread %s', current)
        if not _Namespace.has_key(current):
            _Namespace[current] = {}
        if not _Stacks.has_key(current):
            _Stacks[current] = []
        _Stacks[current].append(_Namespace[current])
        _Namespace[current] = copy.copy(_Namespace[current])

    def _end(self):
        current = threading.currentThread()
        logInfo('ending context in thread %s', current)
        if not _Stacks.has_key(current):
            _Stacks[current] = []
        _Namespace[current] = _Stacks[current].pop()


context = DynamicContext()