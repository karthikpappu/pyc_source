# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\expatriate\model\xs\DecimalType.py
# Compiled at: 2018-01-18 12:29:08
# Size of source mod 2**32: 995 bytes
import logging
from ..decorators import *
from .AnySimpleType import AnySimpleType
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class DecimalType(AnySimpleType):

    def parse_value(self, value):
        return float(value)