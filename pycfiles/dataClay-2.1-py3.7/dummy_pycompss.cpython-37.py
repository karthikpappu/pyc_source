# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dataclay/contrib/dummy_pycompss.py
# Compiled at: 2019-10-28 11:50:26
# Size of source mod 2**32: 948 bytes
""" Class description goes here. """
__author__ = 'Alex Barcelo <alex.barcelo@bsc.es>'
__copyright__ = '2017 Barcelona Supercomputing Center (BSC-CNS)'
INOUT = None
IN = None
OUT = None
FILE_IN = None
FILE_OUT = None
FILE_INOUT = None
CONCURRENT = None

def task(*args, **kwargs):
    return lambda f: f


def constraint(*args, **kwargs):
    return lambda f: f