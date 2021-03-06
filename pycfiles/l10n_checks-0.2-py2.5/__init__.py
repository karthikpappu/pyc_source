# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/mozilla/__init__.py
# Compiled at: 2009-11-23 14:18:57
VERSION = (0, 2, 0, 'final', 0)

def get_short_version():
    version = '%s.%s' % (VERSION[0], VERSION[1])
    if VERSION[2]:
        version = '%s.%s' % (version, VERSION[2])
    if VERSION[3] == 'alpha':
        version = '%sa' % version
    if VERSION[3] == 'beta':
        version = '%sb' % version
    if VERSION[3] == 'rc':
        version = '%sc' % version
    if VERSION[3] != 'final' and VERSION[4]:
        version = '%s%s' % (version, VERSION[4])
    return version


def get_version():
    version = '%s.%s' % (VERSION[0], VERSION[1])
    if VERSION[2]:
        version = '%s.%s' % (version, VERSION[2])
    if VERSION[3:] == ('alpha', 0):
        version = '%s pre-alpha' % version
    else:
        version = '%s %s' % (version, VERSION[3])
        if VERSION[3] != 'final':
            version = '%s %s' % (version, VERSION[4])
    return version