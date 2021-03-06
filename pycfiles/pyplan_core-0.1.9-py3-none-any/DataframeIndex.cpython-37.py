# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fabian/devs/novix/python/pyplan-core/pyplan_core/classes/wizards/DataframeIndex.py
# Compiled at: 2020-04-29 16:08:41
# Size of source mod 2**32: 1040 bytes
import pyplan_core.classes.wizards.BaseWizard as BaseWizard
import pandas as pd, jsonpickle

class Wizard(BaseWizard):

    def __init__(self):
        self.code = 'DataframeIndex'

    def generateDefinition(self, model, params):
        nodeId = params['nodeId']
        if model.existNode(nodeId):
            currentDef = model.getNode(nodeId).definition
            newDef = self.getLastDefinition(currentDef)
            newDef = newDef + '\n# Set index'
            reset_index = ''
            if not isinstance(model.getNode(nodeId).result.index, pd.RangeIndex):
                reset_index = '.reset_index()'
            if params is not None and 'columns' in params and len(params['columns']) > 0:
                newDef = newDef + f"\nresult = _df{reset_index}.set_index({params['columns']})"
            else:
                newDef = newDef + f"\nresult = _df{reset_index}"
            model.getNode(nodeId).definition = self.formatDefinition(newDef)
            return 'ok'
        return ''