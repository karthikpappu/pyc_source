# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpDcc/libs/qt/managers/inputs.py
# Compiled at: 2020-04-26 16:40:12
# Size of source mod 2**32: 1755 bytes
"""
Module that contains implementation for inputs manager
"""
from __future__ import print_function, division, absolute_import
from collections import defaultdict
from tpDcc import register
from tpDcc.libs.python import decorators
from tpDcc.libs.qt.core import input

class InputManager(object):

    def __init__(self):
        self._actions = defaultdict(list)
        self._register_default_inputs()

    def __getitem__(self, key):
        if key in self._actions:
            return self._actions[key]
        else:
            return list()

    def __contains__(self, item):
        return item.get_name() in self._actions

    def get_data(self):
        return self._actions

    def register_action(self, action):
        if action not in self._actions[action.get_name()]:
            self._actions[action.get_name()].append(action)

    def load_from_data(self, data):
        for action_name, action_variants in data.items():
            for variant in action_variants:
                action_instance = input.InputAction().from_dict(variant)
                self.register_action(action_instance)

    def serialize(self):
        result = defaultdict(list)
        for action_name in self._actions:
            for action_variant in self._actions[action_name]:
                result[action_name].append(action_variant.to_dict())

        return result

    def _register_default_inputs(self):
        """
        Internal function that can be overriden to register default inputs
        """
        pass


@decorators.Singleton
class InputsManagerSingleton(InputManager, object):

    def __init__(self):
        InputManager.__init__(self)


register.register_class('InputsMgr', InputsManagerSingleton)