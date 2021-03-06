# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sfs/helper.py
# Compiled at: 2018-12-25 05:10:17
# Size of source mod 2**32: 3547 bytes
import collections, functools
import sfs.exceptions as exceptions
import sfs.log_utils as log

class Disallowed(exceptions.SFSException):
    __doc__ = 'Exception class for attempts to perform restricted operations'


def untested(x):
    """Decorator to mark a class or function as untested"""
    log.logger.warn('A component has been marked untested: %s', x.__name__)
    return x


def wraps_class(cls):
    """
    Updates attributes of wrapper class to match that of wrapped class similar to what functools.wraps does for
    functions
    """

    def decorator(wrapper):
        for attr in functools.WRAPPER_ASSIGNMENTS:
            if hasattr(cls, attr):
                setattr(wrapper, attr, getattr(cls, attr))

        return wrapper

    return decorator


def frozen(cls):
    """Marks a class as readonly after instantiation"""

    @functools.wraps(cls, updated=[])
    class FrozenClassWrapper(cls):

        def __init__(self, *args, **kwargs):
            (cls.__init__)(self, *args, **kwargs)
            self._frozen = True

        def __setattr__(self, key, value):
            if hasattr(self, '_frozen'):
                if self._frozen is True:
                    raise Disallowed('Cannot update frozen object of class "{}"'.format(type(self).__name__))
            cls.__setattr__(self, key, value)

    return FrozenClassWrapper


def has_cached_methods(cls):
    """Enables caching on class methods"""

    @wraps_class(cls)
    class CachedMethodsWrapper(cls):

        def __init__(self, *args, **kwargs):
            (cls.__init__)(self, *args, **kwargs)
            self._cached_methods = collections.defaultdict(collections.OrderedDict)

    return CachedMethodsWrapper


def cached_method(cache_size=100):
    """
    Decorator to cache the output of class method by its positional arguments
    Up tp 'cache_size' values are cached per method and entries are remvoed in a FIFO order
    """

    def decorator(fn):

        @functools.wraps(fn)
        def wrapper(self, *args, **kwargs):
            _dict = self._cached_methods[fn.__name__]
            if args in _dict:
                return _dict[args]
            res = fn(self, *args, **kwargs)
            if len(_dict) >= cache_size:
                _dict.popitem(False)
            _dict[args] = res
            return res

        return wrapper

    return decorator


def with_default(val_or_func, default):
    if callable(val_or_func):
        return lambda val:         if val is None:
default # Avoid dead code: val_or_func(val)
    if val_or_func is None:
        return default
    return val_or_func


def get_readable_size(size_bytes):
    """Convert size in bytes to human readable string"""
    temp = size_bytes
    units = ['Bytes', 'kB', 'MB', 'GB']
    for x in range(len(units)):
        if temp >= 1024:
            if x < len(units) - 1:
                temp = float(temp) / 1024
                continue
        break

    return '%.2f %s' % (temp, units[x])


class ConstantsMetaClass(type):
    __doc__ = 'Metaclass to prevent modification of class attributes'

    def __setattr__(self, key, value):
        raise Disallowed('Cannot modify constant class')


def constant_class(cls):
    """
    Decorator to mark a class as a constant class
    Constant classes cannot be instantiated and their class attributes cannot be updated
    """

    class ConstantClassWrapper(cls, metaclass=ConstantsMetaClass):

        def __new__(cls):
            raise Disallowed('Cannot instantiate constant class')

    return ConstantClassWrapper