# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.5/site-packages/graphite/Num.py
# Compiled at: 2008-02-01 07:52:17
"""This is a compatibility module, allowing python to work
with either scipy, Numeric, or numarray.
It tries to import them, in that order, only reporting
an error if none are available.

Note that this does not pretend to solve all compatibility
problems; it just tries importing all three, so you can only
count on the lowest common denominator.
"""

class _delayed_import(object):

    def __init__(self, name, aliases=[]):
        self.name = name
        self.mod = None
        self.aliases = aliases
        return

    def __getattribute__(self, aname):
        mod = object.__getattribute__(self, 'mod')
        if mod is None:
            mname = object.__getattribute__(self, 'name')
            mod = __import__(mname)
            a = mname.split('.')
            for dot in a[1:]:
                mod = getattr(mod, dot)

            self.mod = mod
            for (nn, on) in object.__getattribute__(self, 'aliases'):
                setattr(mod, nn, getattr(mod, on))

        return getattr(mod, aname)


array = None
try:
    from numpy import *
    LA = _delayed_import('numpy.linalg', [
     ('linear_least_squares', 'lstsq'),
     ('singular_value_decomposition', 'svd')])
    RA = _delayed_import('numpy.random')
    FFT = _delayed_import('numpy.fft', [
     ('inverse_fft', 'ifft'), ('real_fft', 'rfft'),
     ('inverse_real_fft', 'irfft')])
    Float = double
    Int = int0
    Int32 = int32
    Int16 = int16
    Int8 = int8
    Complex = complex_
    arrayrange = arange
    matrixmultiply = dot
    outerproduct = outer
    NewAxis = newaxis
except ImportError:
    pass

if array is None:
    try:
        from Numeric import *
        RA = _delayed_import('RandomArray')
        LA = _delayed_import('LinearAlgebra')
        FFT = _delayed_import('FFT')
    except ImportError:
        pass

if array is None:
    try:
        from numarray import *
    except ImportError:
        raise ImportError, 'No module named either numpy, Numeric or numarray'

assert FFT
assert LA
assert RA