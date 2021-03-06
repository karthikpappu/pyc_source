# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpDcc/libs/qt/core/formatters.py
# Compiled at: 2020-04-15 12:12:43
# Size of source mod 2**32: 2317 bytes
"""
Utility module that contains functions related with formatters
"""
from __future__ import print_function, division, absolute_import
from singledispatch import singledispatch

def apply_formatter(formatter, *args, **kwargs):
    """
    Used by QAbstractModel data method
    Configures a formatter for one field, apply the formatter with the new index data
    :param formatter: formatter. If can be None/dict/callback or just any type of value
    :param args:
    :param kwargs:
    :return:
    """
    if formatter is None:
        return args[0]
    else:
        if isinstance(formatter, dict):
            return formatter.get(args[0], None)
        if callable(formatter):
            return formatter(*args, **kwargs)
        return formatter


def overflow_format(num, overflow):
    """
    Returns string of the given integer. If the integer is large than given overflow, '{overflow}+' is returned
    :param num: int
    :param overflow: int
    :return: str
    """
    if not isinstance(num, int):
        raise ValueError('Input argument "num" should be int type, but get "{}"'.format(type(num)))
    if not isinstance(overflow, int):
        raise ValueError('Input argument "overflow" should be int type, but get "{}"'.format(type(num)))
    if num <= overflow:
        return str(num)
    else:
        return '{}+'.format(overflow)


@singledispatch
def display_formatter(input_other_type):
    """
    Used by QAbstractItemModel data method for Qt.DisplayRole
    Format any input value to a string
    :param input_other_type:
    :return: str
    """
    return str(input_other_type)


@display_formatter.register(type(None))
def _(input_none):
    return '--'


@display_formatter.register(int)
def _(input_int):
    return str(input_int)


@display_formatter.register(float)
def _(input_float):
    return '{:.2f}'.format(round(input_float, 2))


@display_formatter.register(dict)
def _(input_dict):
    if 'name' in input_dict.keys():
        return display_formatter(input_dict.get('name'))
    else:
        if 'code' in input_dict.keys():
            return display_formatter(input_dict.get('code'))
        return str(input_dict)


@display_formatter.register(list)
def _(input_list):
    result = list()
    for i in input_list:
        result.append(display_formatter(i))

    return '.'.join(result)