# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/py3o/types/json/encoder.py
# Compiled at: 2016-04-07 08:08:05
# Size of source mod 2**32: 1386 bytes
import datetime, json, six
from py3o.types import Py3oInteger

class Py3oJSONEncoder(json.JSONEncoder):
    __doc__ = 'A JSON encoder intended to be used alongside :class:`.Py3oJSONDecoder`.\n\n    .. seealso:: :class:`json.JSONEncoder`\n    '

    def iterencode(self, o, _one_shot=False):
        if six.PY2:
            old_str_method = Py3oInteger.__str__
            Py3oInteger.__str__ = int.__repr__
        try:
            res = super(Py3oJSONEncoder, self).iterencode(o, _one_shot=_one_shot)
        finally:
            if six.PY2:
                Py3oInteger.__str__ = old_str_method

        return res

    def default(self, o):
        if isinstance(o, datetime.datetime):
            res = {'_py3o': 'dt',  'val': o.strftime('%Y%m%d%H%M%S')}
        else:
            if isinstance(o, datetime.date):
                res = {'_py3o': 'date',  'val': o.strftime('%Y%m%d')}
            else:
                if isinstance(o, datetime.time):
                    res = {'_py3o': 'time',  'val': o.strftime('%H%M%S')}
                else:
                    res = super(Py3oJSONEncoder, self).default(o)
        return res