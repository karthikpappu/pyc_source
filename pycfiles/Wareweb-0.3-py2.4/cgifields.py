# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/wareweb/cgifields.py
# Compiled at: 2006-10-22 17:17:11
from UserDict import UserDict
from paste import httpexceptions

class HTTPVariableNotFound(httpexceptions.HTTPBadRequest, KeyError):
    """
    Raised when a form variable can't be found.  Catching either of
    HTTPBadRequest or KeyError will work, plus this will turn into a
    better response when a variable isn't found.
    """
    __module__ = __name__


class Fields(UserDict):
    __module__ = __name__

    def __init__(self, field_dict):
        self.data = field_dict

    def __getattr__(self, attr):
        if attr.startswith('_'):
            raise AttributeError
        return self.data[attr]

    def __getitem__(self, key):
        try:
            return self.data[key]
        except KeyError:
            raise HTTPVariableNotFound('The form variable %r was not received' % key)

    def __contains__(self, key):
        return key in self.data

    def __iter__(self):
        return iter(self.data)

    def getlist(self, name):
        """
        Return the named item as a list ([] if name not found,
        [self[name]] if only one field passed in).
        """
        v = self.data.get(name, [])
        if isinstance(v, list):
            return v
        return [
         v]

    def itemlist(self):
        """
        Return a list of (name, [values...]).  Like .items(),
        except all values becomes a list (like .getlist()).
        """
        items = []
        for (name, value) in self.iteritems():
            if isinstance(value, list):
                items.append((name, value))
            else:
                items.append((name, [value]))

        return items

    __str__ = UserDict.__repr__