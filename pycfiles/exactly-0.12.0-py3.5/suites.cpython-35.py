# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/test_suite/instruction_set/sections/suites.py
# Compiled at: 2019-09-20 02:11:24
# Size of source mod 2**32: 2240 bytes
import stat
from pathlib import Path
from typing import List
from exactly_lib.definitions.test_suite import file_names
from exactly_lib.section_document.element_parsers.section_element_parsers import standard_syntax_element_parser, InstructionWithoutDescriptionParser, InstructionParserWithoutSourceFileLocationInfo
from exactly_lib.section_document.parse_source import ParseSource
from exactly_lib.section_document.section_element_parsing import SectionElementParser
from exactly_lib.test_suite.instruction_set import utils
from exactly_lib.test_suite.instruction_set.instruction import Environment, TestSuiteFileReferencesInstruction, FileNotAccessibleSimpleError

def new_parser() -> SectionElementParser:
    return standard_syntax_element_parser(InstructionWithoutDescriptionParser(_SuitesSectionParser()))


class SuitesSectionInstruction(TestSuiteFileReferencesInstruction):

    def __init__(self, resolver: utils.FileNamesResolver):
        self._resolver = resolver

    def resolve_paths(self, environment: Environment) -> List[Path]:
        return self._resolver.resolve(environment)


class _SuitesSectionParser(InstructionParserWithoutSourceFileLocationInfo):

    def parse_from_source(self, source: ParseSource) -> SuitesSectionInstruction:
        resolver = utils.parse_file_names_resolver(source, regular_file_or_default_suite_file)
        return SuitesSectionInstruction(resolver)


def regular_file_or_default_suite_file(path: Path) -> Path:
    try:
        stat_mode = path.stat().st_mode
    except FileNotFoundError:
        raise FileNotAccessibleSimpleError(path, utils.ERR_MSG__NOT_EXISTS)

    if stat.S_ISREG(stat_mode):
        return path
    if stat.S_ISDIR(stat_mode):
        suite_file_path = path / file_names.DEFAULT_SUITE_FILE
        if suite_file_path.is_file():
            return suite_file_path
        raise FileNotAccessibleSimpleError(path, utils.ERR_MSG__DIR_WO_DEFAULT_SUITE)
    else:
        raise FileNotAccessibleSimpleError(path, utils.ERR_MSG__NOT_REG_NOT_DIR)