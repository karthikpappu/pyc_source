# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\expatriate\model\xs\AnyTypeType.py
# Compiled at: 2018-01-18 12:28:28
# Size of source mod 2**32: 1237 bytes
import logging
from ..decorators import *
from ..Model import Model
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class AnyTypeType(Model):

    def get_defs(self, schema, top_level):
        model_map = {'elements':[],  'attributes':{}}
        for t in self.tags:
            defs = t.get_defs(schema, top_level)
            model_map['elements'].extend(defs['elements'])
            model_map['attributes'].update(defs['attributes'])

        return model_map