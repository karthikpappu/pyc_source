# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/bfnet/__init__.py
# Compiled at: 2015-12-05 10:56:06
# Size of source mod 2**32: 160 bytes
from .Net import Net
from .Butterfly import Butterfly
from .BFHandler import ButterflyHandler
from . import packets
get_handler = ButterflyHandler.get_handler