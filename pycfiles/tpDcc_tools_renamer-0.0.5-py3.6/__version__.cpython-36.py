# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpDcc/tools/renamer/__version__.py
# Compiled at: 2020-04-11 22:50:40
# Size of source mod 2**32: 516 bytes
"""
Version module for tpDcc-tools-renamer
"""
from __future__ import print_function, division, absolute_import
__author__ = 'Tomas Poveda'
__license__ = 'MIT'
__maintainer__ = 'Tomas Poveda'
__email__ = 'tpovedatd@gmail.com'
__version__ = None

def get_version():
    global __version__
    if __version__:
        return __version__
    else:
        from ._version import get_versions
        __version__ = get_versions()['version']
        del get_versions
        return __version__