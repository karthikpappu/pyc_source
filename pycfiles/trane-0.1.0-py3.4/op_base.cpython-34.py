# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/trane/ops/op_base.py
# Compiled at: 2018-04-05 13:16:30
# Size of source mod 2**32: 3226 bytes
import json
from ..utils.table_meta import TableMeta as TM
__all__ = [
 'OpBase']
import logging

class OpBase(object):
    __doc__ = 'Super class of all operations. \n        All operations should have REQUIRED_PARAMETERS and IOTYPES.\n\n    IOTYPES is a list of possible input and output type pairs.\n        For example `greater` can operate on int and str and output bool.\n        [(int, bool), (str, bool), ...]\n\n    REQUIRED_PARAMETERS is a list of parameter and type dicts. \n        REQUIRED_PARAMETERS have the same length as IOTYPES.\n        With different input types, parameters may have different types. \n        For example the REQUIRED_PARAMETERS of `greater` is\n        [\\{threshold: int\\}, \\{threshold: str\\}, ...]\n\n    input_type and otype are the actual input and output type.\n        hyper_parameter_settings is a dict of parameter name and value.\n\n    '
    REQUIRED_PARAMETERS = None
    IOTYPES = None

    def __init__(self, column_name):
        """Initalization of all operations. Subclasses shouldn't have their own init.
            This function checks whether REQUIRED_PARAMETERS and IOTYPES are defined and compatable. 

        args:
            column_name: the column this operation is applied on. 

        """
        self.column_name = column_name
        self.input_type = self.output_type = None
        self.hyper_parameter_settings = {}

    def op_type_check(self, table_meta):
        """Data type check for the operation. 
            Operations may change the data type of a column, eg. int -> bool. 
            One operation can only be applied on a few data types, eg. `greater` can 
            be applied on int but can't be applied on bool.
            This function checks whether current operation can be applied on the data.
            It returns the updated TableMeta for next operation.

        args:
            table_meta: table meta before this operation.

        returns:
            TableMeta: table meta after this operation. None if not compatable.

        """
        self.input_type = table_meta.get_type(self.column_name)
        for idx, (input_type, output_type) in enumerate(self.IOTYPES):
            if self.input_type == input_type:
                self.output_type = output_type
                table_meta.set_type(self.column_name, output_type)
                return table_meta

    def set_hyper_parameter(self, hyper_parameter):
        for parameter_requirement in self.REQUIRED_PARAMETERS:
            for parameter_name, parameter_type in parameter_requirement.items():
                self.hyper_parameter_settings[parameter_name] = hyper_parameter

    def __call__(self, dataframe):
        return self.execute(dataframe)

    def execute(self, dataframe):
        raise NotImplementedError

    def __hash__(self):
        return hash((type(self).__name__, self.column_name))

    def __str__(self):
        return '%s(%s)' % (type(self).__name__, self.column_name)

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(self, other.__class__):
            return self.__dict__ == other.__dict__
        return False