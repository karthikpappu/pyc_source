# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ctyfoxylos/SBP/python/hashivaultlib/hashivaultlib/_version.py
# Compiled at: 2019-01-21 04:59:41
# Size of source mod 2**32: 2108 bytes
"""
Manages the version of the package.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""
import os
__author__ = 'Costas Tyfoxylos <ctyfoxylos@schubergphilis.com>'
__docformat__ = 'google'
__date__ = '2018-05-25'
__copyright__ = 'Copyright 2018, Costas Tyfoxylos'
__license__ = 'MIT'
__maintainer__ = 'Costas Tyfoxylos'
__email__ = '<ctyfoxylos@schubergphilis.com>'
__status__ = 'Development'
VERSION_FILE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.VERSION'))
LOCAL_VERSION_FILE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '.VERSION'))
try:
    with open(VERSION_FILE_PATH) as (f):
        __version__ = f.read()
except IOError:
    with open(LOCAL_VERSION_FILE_PATH) as (f):
        __version__ = f.read()