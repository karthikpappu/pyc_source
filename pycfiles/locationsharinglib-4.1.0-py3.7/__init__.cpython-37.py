# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/costas/Projects/python/locationsharinglib/locationsharinglib/__init__.py
# Compiled at: 2019-09-01 15:53:30
# Size of source mod 2**32: 2033 bytes
"""
locationsharinglib package.

Import all parts from locationsharinglib here

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html
"""
from ._version import __version__
from .locationsharinglibexceptions import InvalidCookies, InvalidData
from .locationsharinglib import Service, Person
__author__ = 'Costas Tyfoxylos <costas.tyf@gmail.com>'
__docformat__ = 'google'
__date__ = '2017-12-24'
__copyright__ = 'Copyright 2017, Costas Tyfoxylos'
__license__ = 'MIT'
__maintainer__ = 'Costas Tyfoxylos'
__email__ = '<costas.tyf@gmail.com>'
__status__ = 'Development'
assert __version__
assert Service
assert Person
assert InvalidCookies
assert InvalidData