# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/test_general.py
# Compiled at: 2020-03-11 21:48:06
# Size of source mod 2**32: 242 bytes
"""
Module that contains general tests for artellapipe-libs-alembic
"""
import pytest
from artellapipe.libs.alembic import __version__

def test_version():
    assert __version__.__version__