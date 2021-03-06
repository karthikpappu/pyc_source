# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/symbol/data/data_type_sdv.py
# Compiled at: 2019-12-27 10:07:41
# Size of source mod 2**32: 1634 bytes
from typing import List
from exactly_lib.symbol.path_resolving_environment import PathResolvingEnvironmentPreOrPostSds
from exactly_lib.symbol.sdv_structure import SymbolDependentValue
from exactly_lib.symbol.symbol_usage import SymbolReference
from exactly_lib.test_case_file_structure.dir_dependent_value import DependenciesAwareDdv
from exactly_lib.type_system.value_type import TypeCategory, DataValueType, ValueType
from exactly_lib.util.symbol_table import SymbolTable

class DataTypeSdv(SymbolDependentValue):
    __doc__ = ' Base class for symbol values - values that represent data.'

    @property
    def type_category(self) -> TypeCategory:
        return TypeCategory.DATA

    @property
    def data_value_type(self) -> DataValueType:
        raise NotImplementedError('abstract method')

    @property
    def value_type(self) -> ValueType:
        raise NotImplementedError('abstract method')

    @property
    def references(self) -> List[SymbolReference]:
        raise NotImplementedError('abstract method')

    def resolve(self, symbols: SymbolTable) -> DependenciesAwareDdv:
        """
        Resolves the value given a symbol table.
        :rtype: Depends on the concrete value.
        """
        raise NotImplementedError('abstract method')

    def resolve_value_of_any_dependency(self, environment: PathResolvingEnvironmentPreOrPostSds):
        """
        Short cut for resolving the value_of_any_dependency
        """
        return self.resolve(environment.symbols).value_of_any_dependency(environment.tcds)


def get_data_value_type(sdv: DataTypeSdv) -> DataValueType:
    return sdv.data_value_type