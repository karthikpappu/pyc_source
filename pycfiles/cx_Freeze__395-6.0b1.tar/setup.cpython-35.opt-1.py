# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \.\cx_Freeze\samples\zope\setup.py
# Compiled at: 2019-08-29 22:24:39
# Size of source mod 2**32: 767 bytes
import sys
from cx_Freeze import setup, Executable
options = {'build_exe': {'namespace_packages': ['zope']}}
executables = [
 Executable('qotd.py')]
setup(name='QOTD sample', version='1.0', description='QOTD sample for demonstrating use of namespace packages', options=options, executables=executables)