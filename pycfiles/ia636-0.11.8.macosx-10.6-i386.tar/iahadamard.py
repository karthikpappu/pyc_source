# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/robertoalotufo/Library/Enthought/Canopy_32bit/User/lib/python2.7/site-packages/ia636/iahadamard.py
# Compiled at: 2014-08-21 22:30:04
from numpy import *

def iahadamard(f):
    from iahadamardmatrix import iahadamardmatrix
    f = asarray(f).astype(float64)
    if len(f.shape) == 1:
        f = f[:, newaxis]
    m, n = f.shape
    A = iahadamardmatrix(m)
    if n == 1:
        F = dot(A, f)
    else:
        B = iahadamardmatrix(n)
        F = dot(dot(A, f), transpose(B))
    return F