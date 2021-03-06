# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pretty_number/_pretty_number.py
# Compiled at: 2018-11-24 23:17:17
# Size of source mod 2**32: 660 bytes
from math import floor, log10
_to_super = dict(zip('0123456789-', '⁰¹²³⁴⁵⁶⁷⁸⁹⁻'))

def pretty_float(f, significant=4):
    if significant is None:
        if decimal is None:
            decimal = 3
    exponet = floor(log10(f))
    s_exp = ''.join([_to_super[i] for i in str(exponet)])
    m = f * 10 ** (-exponet)
    if -3 < exponet < significant:
        return f"{{:,.{significant - exponet - 1}f}}".format(f)
    return f"%1.{significant - 1}f × 10{s_exp}" % m


def pretty_int(i):
    return '{:,}'.format(i)


def pretty_number(n):
    if isinstance(n, int):
        return pretty_int(n)
    if isinstance(n, float):
        return pretty_float(n)