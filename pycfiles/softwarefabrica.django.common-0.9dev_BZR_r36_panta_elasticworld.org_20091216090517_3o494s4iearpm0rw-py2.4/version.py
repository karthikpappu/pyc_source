# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/softwarefabrica/django/common/version.py
# Compiled at: 2009-01-17 04:03:48
VERSION = (0, 9, 'dev')
from sflib.version import get_version as sf_get_version, get_version_setuptools as sf_get_version_setuptools

def get_version(*args, **kwargs):
    kwargs['VERSION'] = VERSION
    kwargs['path'] = __file__
    kwargs['cr_dirname'] = __file__
    return sf_get_version(*args, **kwargs)


def get_version_setuptools(*args, **kwargs):
    kwargs['VERSION'] = VERSION
    kwargs['path'] = __file__
    kwargs['cr_dirname'] = __file__
    return sf_get_version_setuptools(*args, **kwargs)