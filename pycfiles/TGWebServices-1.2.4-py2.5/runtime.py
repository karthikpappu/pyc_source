# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tgwebservices/runtime.py
# Compiled at: 2010-08-30 04:23:04
"""Runtime registration data."""
import inspect, types, base64
from turbojson import jsonify
from datetime import datetime, date, time

class typedproperty(property):
    """Wraps the standard Python property function allowing you
    to specify what return type will be coming from your property's
    getter method."""

    def __init__(self, type, *args, **kw):
        self.type = type
        super(typedproperty, self).__init__(*args, **kw)


class unsigned(object):
    """Represents an unsigned integer to the outside world. Within
    Python, it just creates an int."""

    def __new__(cls, value=None):
        if value is not None:
            if value < 0:
                from tgwebservices.base import ClientError
                raise ClientError('Value of %s is not an unsigned integer' % value)
            return int(value)
        else:
            return int()
        return


class binary(object):
    """Represents base64-encoded binary datas to the outside world."""

    def __init__(self, value=None):
        self.data = value

    def base64(self):
        if self.data is not None:
            return base64.encodestring(self.data)
        return

    def __json__(self):
        return self.base64()

    def __str__(self):
        return self.data


primitives = set([int, basestring, str, unicode, float, bool, list, dict,
 long, typedproperty, unsigned,
 datetime, date, time,
 binary])

@jsonify.jsonify.when('isinstance(obj, datetime)')
def jsonify_datetime(obj):
    return obj.isoformat()


@jsonify.jsonify.when('isinstance(obj, date)')
def jsonify_date(obj):
    return obj.isoformat()


@jsonify.jsonify.when('isinstance(obj, time)')
def jsonify_time(obj):
    return obj.isoformat()


class FunctionInfo(object):
    """Keeps track of information about a function that is available for
    web services use.
    """
    return_type = basestring
    _params = None
    input_types = {}

    def __init__(self, params, defaults):
        self.params = params
        if defaults:
            optional = [ params[i] for i in range(len(params) - len(defaults), len(params))
                       ]
            self.optional = set(optional)
        else:
            self.optional = []
        self.complex_types = set()

    def _set_params(self, value):
        if value and value[0] == 'self':
            value = value[1:]
        self._params = value

    params = property(lambda self: self._params, _set_params)

    def __repr__(self):
        return 'Return type: %s, params: %s' % (self.return_type, self.params)


def register(func):
    """Registers a function as available for web services. You can call this
    repeatedly and will get back the same FunctionInfo object each time.
    
    @param func Function to register
    @return a FunctionInfo object with the information saved for this
            function."""
    if not hasattr(func, '_ws_func_info'):
        argspec = inspect.getargspec(func)
        func._ws_func_info = FunctionInfo(argspec[0], argspec[3])
    return func._ws_func_info


def ctvalues(cls):
    """Inspects a class for the defined default values. This is used to
    figure out the types of attributes that instances of the class will
    be expected to have (to provide useful information for statically
    typed languages). It will strip out any attribute that starts with _,
    any method, and any property that is not a typedproperty.
    
    @param cls class to inspect
    @return list of keys that are likely holders of useful data"""
    return [ key for key in dir(cls) if not key.startswith('_') if not isinstance(getattr(cls, key), types.MethodType) if not type(getattr(cls, key)) == property
           ]


def _setup_new_type(cls):
    cls._type_dependents = 0

    @jsonify.jsonify.when('isinstance(obj, cls)')
    def jsonify_cls(obj):
        simplified = dict()
        for key in ctvalues(cls):
            val = getattr(obj, key)
            if val is not None and type(val) not in primitives:
                val = jsonify.jsonify(val)
            simplified[key] = val

        return simplified


def register_complex_type(fi, cls):
    """Remembers a complex type (user-defined class) that has been discovered and 
    also discovers any complex types that are referred  to be the given type.
    Additionally, this will keep track of how many classes depend on a given
    class in the _type_dependencies class variable. This is used as a crude
    mechanism for determining an appropriate order for types to appear in when
    being defined for consumption by clients.
    
    @param fi the FunctionInfo object that will hold the complex types
    @param cls The class to add and inspect"""
    if not cls or cls in fi.complex_types:
        return
    if not hasattr(cls, '_type_dependents'):
        _setup_new_type(cls)
    fi.complex_types.add(cls)
    for key in ctvalues(cls):
        checkitem = getattr(cls, key)
        if isinstance(checkitem, list):
            checkitem = checkitem[0]
        if not isinstance(checkitem, type):
            checkitem = checkitem.__class__
        if checkitem != types.NoneType and checkitem not in primitives:
            if not hasattr(checkitem, '_type_dependents'):
                _setup_new_type(checkitem)
            checkitem._type_dependents += 1
            register_complex_type(fi, checkitem)