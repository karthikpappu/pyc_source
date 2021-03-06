# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\User\AppData\Local\Temp\pip-install-oj_abz_z\hypothesis\hypothesis\internal\cathetus.py
# Compiled at: 2020-01-12 08:06:33
# Size of source mod 2**32: 2442 bytes
from math import fabs, inf, isinf, isnan, nan, sqrt
from sys import float_info

def cathetus(h, a):
    """Given the lengths of the hypotenuse and a side of a right triangle,
    return the length of the other side.

    A companion to the C99 hypot() function.  Some care is needed to avoid
    underflow in the case of small arguments, and overflow in the case of
    large arguments as would occur for the naive implementation as
    sqrt(h*h - a*a).  The behaviour with respect the non-finite arguments
    (NaNs and infinities) is designed to be as consistent as possible with
    the C99 hypot() specifications.

    This function relies on the system ``sqrt`` function and so, like it,
    may be inaccurate up to a relative error of (around) floating-point
    epsilon.

    Based on the C99 implementation https://github.com/jjgreen/cathetus
    """
    if isnan(h):
        return nan
    elif isinf(h):
        if isinf(a):
            return nan
            return inf
            h = fabs(h)
            a = fabs(a)
            if h < a:
                return nan
            if h > sqrt(float_info.max):
                if h > float_info.max / 2:
                    b = sqrt(h - a) * sqrt(h / 2 + a / 2) * sqrt(2)
        else:
            b = sqrt(h - a) * sqrt(h + a)
    elif h < sqrt(float_info.min):
        b = sqrt(h - a) * sqrt(h + a)
    else:
        b = sqrt((h - a) * (h + a))
    return min(b, h)