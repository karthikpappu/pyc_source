# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/robertoalotufo/Library/Enthought/Canopy_32bit/User/lib/python2.7/site-packages/ia636/iaind2sub.py
# Compiled at: 2014-08-21 22:30:04
from numpy import *

def iaind2sub(dim, i):
    x = i / dim[1]
    y = i % dim[1]
    return (x, y)