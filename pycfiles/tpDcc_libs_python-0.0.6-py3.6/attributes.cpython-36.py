# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpDcc/libs/python/attributes.py
# Compiled at: 2020-05-02 23:38:35
# Size of source mod 2**32: 1722 bytes
"""
Module that contains utility functions related with attributes
"""
from __future__ import print_function, division, absolute_import

def attr_type(attr_value):
    """
    Determines the attribute type based on the given value
    :param attr_value: variant, attribute value
    :return: str, attribute type
    """
    from tpDcc.libs.python import python
    if python.is_none(attr_value):
        return 'null'
    if python.is_list(attr_value):
        return list_attr_types(attr_value)
    if python.is_bool(attr_value):
        return 'bool'
    if python.is_string(attr_value):
        return 'str'
    else:
        if python.is_number(attr_value):
            if type(attr_value) is float:
                return 'float'
            if type(attr_value) is int:
                return 'int'
        return 'unknown'


def list_attr_types(s):
    """
    Return a string type for the value
    """
    from tpDcc.libs.python import python
    if not python.is_list(s):
        return 'unknown'
    else:
        for typ in [str, int, float, bool]:
            if all(isinstance(n, typ) for n in s):
                return '%s%d' % (typ.__name__, len(s))

        if False not in list(set([python.is_number(x) for x in s])):
            return 'float%d' % len(s)
        return 'unknown'


def auto_convert_attr(attr_value):
    """
    Converts a given attribute value to it's given type
    """
    atype = attr_type(attr_value)
    if atype == 'str':
        return str(attr_value)
    if atype == 'bool':
        return bool(attr_value)
    if atype == 'float':
        return float(attr_value)
    else:
        if atype == 'int':
            return int(attr_value)
        return attr_value