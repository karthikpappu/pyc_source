# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-intel/egg/kyoka/value_function/base_state_value_function.py
# Compiled at: 2016-10-26 09:22:48
from kyoka.value_function.base_value_function import BaseValueFunction

class BaseStateValueFunction(BaseValueFunction):

    def calculate_value(self, state):
        err_msg = self.__build_err_msg('calculate_value')
        raise NotImplementedError(err_msg)

    def update_function(self, state, new_value):
        err_msg = self.__build_err_msg('update_function')
        raise NotImplementedError(err_msg)

    def setUp(self):
        pass

    def __build_err_msg(self, msg):
        base_msg = '[ {0} ] class does not implement [ {1} ] method'
        return base_msg.format(self.__class__.__name__, msg)