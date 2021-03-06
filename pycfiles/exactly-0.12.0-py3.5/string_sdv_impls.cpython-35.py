# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/symbol/data/impl/string_sdv_impls.py
# Compiled at: 2019-12-27 10:07:41
# Size of source mod 2**32: 4498 bytes
from typing import Sequence
from exactly_lib.symbol import symbol_usage as su, sdv_structure as struct
from exactly_lib.symbol.data.data_type_sdv import DataTypeSdv
from exactly_lib.symbol.data.list_sdv import ListSdv
from exactly_lib.symbol.data.path_sdv import PathSdv
from exactly_lib.symbol.data.string_sdv import StringFragmentSdv
from exactly_lib.symbol.path_resolving_environment import PathResolvingEnvironmentPreOrPostSds
from exactly_lib.symbol.symbol_usage import SymbolReference
from exactly_lib.type_system.data import string_ddv as sv, concrete_strings as csv
from exactly_lib.type_system.data.concrete_strings import StrValueTransformer, TransformedStringFragmentDdv, StringDdvFragmentDdv
from exactly_lib.type_system.data.list_ddv import ListDdv
from exactly_lib.type_system.data.path_ddv import PathDdv
from exactly_lib.util.symbol_table import SymbolTable

class ConstantStringFragmentSdv(StringFragmentSdv):
    __doc__ = '\n    A fragment that is a string constant.\n    '

    def __init__(self, constant: str):
        self._constant = constant

    @property
    def is_string_constant(self) -> bool:
        return True

    @property
    def string_constant(self) -> str:
        return self._constant

    @property
    def references(self) -> Sequence[SymbolReference]:
        return ()

    def resolve(self, symbols: SymbolTable) -> sv.StringFragmentDdv:
        return csv.ConstantFragmentDdv(self._constant)


class SymbolStringFragmentSdv(StringFragmentSdv):
    __doc__ = '\n    A fragment that represents a reference to a symbol.\n    '

    def __init__(self, symbol_reference: su.SymbolReference):
        self._symbol_reference = symbol_reference

    @property
    def symbol_name(self) -> str:
        return self._symbol_reference.name

    @property
    def references(self) -> Sequence[SymbolReference]:
        return (self._symbol_reference,)

    def resolve(self, symbols: SymbolTable) -> sv.StringFragmentDdv:
        container = symbols.lookup(self._symbol_reference.name)
        assert isinstance(container, struct.SymbolContainer), 'Value in SymTbl must be SymbolContainer'
        value_sdv = container.sdv
        assert isinstance(value_sdv, DataTypeSdv), 'Value must be a DataTypeSdv'
        value = value_sdv.resolve(symbols)
        if isinstance(value, sv.StringDdv):
            return csv.StringDdvFragmentDdv(value)
        if isinstance(value, PathDdv):
            return csv.PathFragmentDdv(value)
        if isinstance(value, ListDdv):
            return csv.ListFragmentDdv(value)
        raise TypeError('Not a {}: {}'.format(str(DataTypeSdv), value))


class PathAsStringFragmentSdv(StringFragmentSdv):

    def __init__(self, path: PathSdv):
        self._path = path

    @property
    def references(self) -> Sequence[SymbolReference]:
        return self._path.references

    def resolve(self, symbols: SymbolTable) -> sv.StringFragmentDdv:
        return csv.PathFragmentDdv(self._path.resolve(symbols))


class ListAsStringFragmentSdv(StringFragmentSdv):

    def __init__(self, list_sdv: ListSdv):
        self._list_sdv = list_sdv

    @property
    def references(self) -> Sequence[SymbolReference]:
        return self._list_sdv.references

    def resolve(self, symbols: SymbolTable) -> sv.StringFragmentDdv:
        return csv.ListFragmentDdv(self._list_sdv.resolve(symbols))


class TransformedStringFragmentSdv(StringFragmentSdv):
    __doc__ = "\n    A fragment who's string is transformed by a function.\n    "

    def __init__(self, string_sdv: StringFragmentSdv, transformer: StrValueTransformer):
        self._string_sdv = string_sdv
        self._transformer = transformer

    @property
    def is_string_constant(self) -> bool:
        return self._string_sdv.is_string_constant

    @property
    def string_constant(self) -> str:
        return self._transformer(self._string_sdv.string_constant)

    def resolve(self, symbols: SymbolTable) -> sv.StringFragmentDdv:
        return TransformedStringFragmentDdv(StringDdvFragmentDdv(self._string_sdv.resolve(symbols)), self._transformer)

    @property
    def references(self) -> list:
        return self._string_sdv.references

    def resolve_value_of_any_dependency(self, environment: PathResolvingEnvironmentPreOrPostSds) -> str:
        return self.resolve(environment.symbols).value_of_any_dependency(environment)