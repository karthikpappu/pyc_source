# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/help/entities/syntax_elements/objects/glob_pattern.py
# Compiled at: 2018-09-19 16:40:01
# Size of source mod 2**32: 2686 bytes
from exactly_lib.common.help.see_also import SeeAlsoUrlInfo
from exactly_lib.definitions.doc_format import syntax_text
from exactly_lib.definitions.entity import syntax_elements
from exactly_lib.help.entities.syntax_elements.contents_structure import syntax_element_documentation
from exactly_lib.util.textformat.structure import lists
from exactly_lib.util.textformat.structure import structures as docs
from exactly_lib.util.textformat.textformat_parser import TextParser
_TP = TextParser()
_HEADER = 'A file name, with ability to match multiple files.\n\n\nPattern matchers:\n'
_DIRECTORY_SPECIFICATIONS_HEADER = 'Directory specifications:'
_FOOTER = "For a literal match, wrap the meta-characters in brackets. For example, '[?]' matches the character '?'.\n\n\nA patterns cannot denote an absolute path.\n"
_PATTERNS = docs.simple_list_with_space_between_elements_and_content([
 docs.list_item(syntax_text('?'), docs.paras('Matches any single character.')),
 docs.list_item(syntax_text('*'), docs.paras('Matches any number of any characters including none.')),
 docs.list_item(syntax_text('[CHARACTERS]'), docs.paras('Matches a single character that is listed in CHARACTERS.   ')),
 docs.list_item(syntax_text('[CHARACTER-CHARACTER]'), docs.paras('Matches a single character in the given range.')),
 docs.list_item(syntax_text('[!CHARACTER-SET]'), docs.paras('Matches a single character NOT in CHARACTER-SET.'))], lists.ListType.ITEMIZED_LIST)
_DIRECTORY_SPECIFICATIONS = docs.simple_list_with_space_between_elements_and_content([
 docs.list_item(syntax_text('**'), docs.paras('The directory where the pattern is applied, and all subdirectories, recursively.')),
 docs.list_item(syntax_text('/'), docs.paras('Directory separator.'))], lists.ListType.ITEMIZED_LIST)
DOCUMENTATION = syntax_element_documentation(None, syntax_elements.GLOB_PATTERN_SYNTAX_ELEMENT, _TP.fnap(_HEADER) + [_PATTERNS] + _TP.paras(_DIRECTORY_SPECIFICATIONS_HEADER) + [_DIRECTORY_SPECIFICATIONS] + _TP.fnap(_FOOTER), [], [], [
 SeeAlsoUrlInfo('Python file name matching', 'file:///usr/local/share/doc/python3/library/fnmatch.html'),
 SeeAlsoUrlInfo('Glob patterns on Wikipedia', 'https://en.wikipedia.org/wiki/Glob_(programming)#Unix')])