# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/symbol/err_msg/error_messages.py
# Compiled at: 2019-12-27 10:07:41
# Size of source mod 2**32: 6328 bytes
from pathlib import Path
from typing import Optional, List, Sequence
from exactly_lib.common.err_msg import rendering
from exactly_lib.common.err_msg import source_location
from exactly_lib.common.err_msg.definitions import Blocks, single_str_block
from exactly_lib.common.report_rendering import text_docs
from exactly_lib.common.report_rendering.text_doc import TextRenderer
from exactly_lib.definitions import type_system
from exactly_lib.section_document.source_location import SourceLocationInfo
from exactly_lib.symbol import symbol_usage as su
from exactly_lib.symbol.data.value_restriction import ErrorMessageWithFixTip
from exactly_lib.symbol.sdv_structure import SymbolContainer, SymbolDependentValue
from exactly_lib.type_system.value_type import ValueType

def duplicate_symbol_definition(already_defined_symbol: Optional[SourceLocationInfo], name: str) -> TextRenderer:
    return text_docs.major_blocks_of_string_blocks(_duplicate_symbol_definition(already_defined_symbol, name))


def undefined_symbol(reference: su.SymbolReference) -> TextRenderer:
    return text_docs.major_blocks_of_string_blocks(_undefined_symbol(reference))


def invalid_type_msg(expected_value_types: List[ValueType], symbol_name: str, container_of_actual: SymbolContainer) -> ErrorMessageWithFixTip:
    actual = container_of_actual.sdv
    if not isinstance(actual, SymbolDependentValue):
        raise TypeError('Symbol table contains a value that is not a {}: {}'.format(type(SymbolDependentValue), str(actual)))
    assert isinstance(actual, SymbolDependentValue)
    header_lines = _invalid_type_header_lines(expected_value_types, actual.value_type, symbol_name, container_of_actual)
    how_to_fix_lines = _invalid_type_how_to_fix_lines(expected_value_types)
    return ErrorMessageWithFixTip(text_docs.single_pre_formatted_line_object('\n'.join(header_lines)), how_to_fix=text_docs.single_pre_formatted_line_object('\n'.join(how_to_fix_lines)))


def defined_at_line__err_msg_lines(definition_source: Optional[SourceLocationInfo]) -> List[str]:
    if definition_source is None:
        return [_WHICH_IS_A_BUILTIN_SYMBOL]
    else:
        blocks = [
         [
          'defined at']] + _definition_source_blocks(definition_source)
        return rendering.blocks_as_lines(blocks)


_WHICH_IS_A_BUILTIN_SYMBOL = 'which is a builtin symbol'
_IS_A_BUILTIN_SYMBOL = 'is a builtin symbol'

def _is_a_builtin_symbol(symbol_name: str) -> str:
    return symbol_name + ' ' + _IS_A_BUILTIN_SYMBOL


def _invalid_type_header_lines--- This code section failed: ---

 L.  71         0  LOAD_GLOBAL              str
                3  LOAD_CONST               ('return',)
                6  LOAD_CLOSURE             'expected'
                9  BUILD_TUPLE_1         1 
               12  LOAD_CODE                <code_object expected_type_str>
               15  LOAD_STR                 '_invalid_type_header_lines.<locals>.expected_type_str'
               18  MAKE_CLOSURE_A_2_0        '0 positional, 0 keyword only, 2 annotated'
               24  STORE_FAST               'expected_type_str'

 L.  80        27  LOAD_STR                 'Illegal type, of symbol "{}"'
               30  LOAD_ATTR                format
               33  LOAD_FAST                'symbol_name'
               36  CALL_FUNCTION_1       1  '1 positional, 0 named'
               39  BUILD_LIST_1          1 
               42  LOAD_GLOBAL              defined_at_line__err_msg_lines
               45  LOAD_FAST                'container'
               48  LOAD_ATTR                source_location
               51  CALL_FUNCTION_1       1  '1 positional, 0 named'
               54  BINARY_ADD       

 L.  82        55  LOAD_STR                 ''

 L.  83        58  LOAD_STR                 'Found    : '
               61  LOAD_GLOBAL              _type_name_of
               64  LOAD_FAST                'actual'
               67  CALL_FUNCTION_1       1  '1 positional, 0 named'
               70  BINARY_ADD       

 L.  84        71  LOAD_STR                 'Expected : '
               74  LOAD_FAST                'expected_type_str'
               77  CALL_FUNCTION_0       0  '0 positional, 0 named'
               80  BINARY_ADD       
               81  BUILD_LIST_3          3 
               84  BINARY_ADD       
               85  STORE_FAST               'ret_val'

 L.  86        88  LOAD_FAST                'ret_val'
               91  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


def _invalid_type_how_to_fix_lines(expected_value_types: list) -> List[str]:
    from exactly_lib.definitions.test_case.instructions import define_symbol
    from exactly_lib.definitions.test_case.instructions.instruction_names import SYMBOL_DEFINITION_INSTRUCTION_NAME
    from exactly_lib.definitions.formatting import InstructionName
    from exactly_lib.definitions.message_rendering import render_paragraph_item
    def_name_emphasised = InstructionName(SYMBOL_DEFINITION_INSTRUCTION_NAME).emphasis
    header = [
     'Define a legal symbol using the {} instruction:'.format(def_name_emphasised),
     '']
    def_instruction_syntax_table = define_symbol.def_syntax_table(expected_value_types)
    return header + _indent_lines('  ', render_paragraph_item(def_instruction_syntax_table))


def _indent_lines(indent: str, lines: Sequence[str]) -> List[str]:
    return [indent + line for line in lines]


def _type_name_of(value_type: ValueType) -> str:
    return type_system.TYPE_INFO_DICT[value_type].identifier


def _duplicate_symbol_definition(already_defined_symbol: Optional[SourceLocationInfo], name: str) -> Blocks:
    header_block = [
     "Symbol `{}' has already been defined:".format(name)]
    def_src_blocks = [[_is_a_builtin_symbol(name)]] if already_defined_symbol is None else _definition_source_blocks(already_defined_symbol)
    return [
     header_block] + def_src_blocks


def _undefined_symbol(reference: su.SymbolReference) -> Blocks:
    from exactly_lib.definitions.formatting import InstructionName
    from exactly_lib.definitions.test_case.instructions.instruction_names import SYMBOL_DEFINITION_INSTRUCTION_NAME
    def_name_emphasised = InstructionName(SYMBOL_DEFINITION_INSTRUCTION_NAME).emphasis
    return [
     [
      "Symbol `{}' is undefined.".format(reference.name)],
     [
      'Define a symbol using the {} instruction.'.format(def_name_emphasised)]]


def _definition_source_blocks(definition_source: SourceLocationInfo) -> Blocks:
    formatter = source_location.default_formatter
    return formatter.source_location_path(Path('.'), definition_source.source_location_path)


def _builtin_or_user_defined_source_blocks(definition_source: Optional[SourceLocationInfo]) -> Blocks:
    if definition_source is None:
        return [
         single_str_block(_WHICH_IS_A_BUILTIN_SYMBOL)]
    else:
        formatter = source_location.default_formatter
        return formatter.source_location_path(Path('.'), definition_source.source_location_path)