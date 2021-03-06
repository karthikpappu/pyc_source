# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/confiture/parser.py
# Compiled at: 2014-05-11 06:19:13
__doc__ = ' Confiture lexer and parser.\n'
import sys
from glob import glob
import ply.lex as lex, ply.yacc as yacc
from confiture.tree import ConfigSection, ConfigValue, Position
UNITS = {'k': 1000, 'M': 1000000, 
   'G': 1000000000, 
   'T': 1000000000000, 
   'P': 1000000000000000, 
   'E': 1000000000000000000, 
   'Z': 1000000000000000000000, 
   'Y': 1000000000000000000000000, 
   'Ki': 1024, 
   'Mi': 1048576, 
   'Gi': 1073741824, 
   'Ti': 1099511627776, 
   'Pi': 1125899906842624, 
   'Ei': 1152921504606846976, 
   'Zi': 1180591620717411303424, 
   'Yi': 1208925819614629174706176}

class ParsingError(Exception):
    """ Error raised when a parsing error occurs.
    """

    def __init__(self, msg, position=None):
        super(ParsingError, self).__init__(msg)
        self.position = position


def default_external_opener(locator):
    """ The default locator used to open included external files.
    """
    parsed_externals = []
    for external in glob(locator):
        try:
            with open(external) as (fexternal):
                external_data = fexternal.read()
        except IOError as err:
            raise ParsingError('Unable to open %s (%s)' % (external, err))

        parser = ConfitureParser(external_data, debug=False, write_tables=False, errorlog=yacc.NullLogger(), input_name=external, external_opener=default_external_opener)
        parsed_externals.append(parser.parse())

    return parsed_externals


class ConfitureLexer(object):
    r""" Lexer for the DotConf format.

    :param \*\*kwargs: arguments to give to the ply lexer

    Usage example::

    >>> lexer = DotConfLexer()
    >>> lexer.input('test { key = yes }')
    >>> print lexer.next()
    """

    def __init__(self, encoding='utf-8', input_name='<unknown>', **kwargs):
        self._lexer = lex.lex(module=self, **kwargs)
        self._encoding = encoding
        self._input_name = input_name

    reserved = {'yes': 'YES', 'no': 'NO', 'include': 'INCLUDE'}
    reserved.update(dict((kw, 'UNIT') for kw in UNITS))
    tokens = ['LBRACE', 'RBRACE', 'NAME', 'TEXT', 'NUMBER',
     'ASSIGN', 'LIST_SEP'] + list(set(reserved.values()))
    t_LBRACE = '{'
    t_RBRACE = '}'
    t_ASSIGN = '='
    t_LIST_SEP = ','
    t_ignore = ' \t'

    def t_NAME(self, token):
        """[a-zA-Z_][a-zA-Z0-9_-]*"""
        token.type = self.reserved.get(token.value, 'NAME')
        if token.type == 'YES':
            token.value = True
        elif token.type == 'NO':
            token.value = False
        elif token.type == 'UNIT':
            token.value = UNITS[token.value]
        return token

    def t_TEXT(self, token):
        r"""(["]([\\]["]|[^"]|)*["]|[\']([\\][\']|[^\'])*[\'])"""
        value = token.value[1:-1].replace('\\' + token.value[0], token.value[0])
        token.value = value
        token.lexer.lineno += value.count('\n')
        return token

    def t_NUMBER(self, token):
        r"""[-+]?[0-9]+(\.[0-9]+)?"""
        if token.value.isdigit():
            token.value = int(token.value)
        else:
            token.value = float(token.value)
        return token

    def t_EOL(self, token):
        r"""[\n]+"""
        token.lexer.lineno += len(token.value)

    def t_COMMENT(self, token):
        """[#].*"""
        pass

    def t_error(self, token):
        position = Position(self._input_name, self._lexer.lineno, self._lexer.lexpos)
        raise ParsingError('Illegal character %r' % token.value[0], position)

    def column(self, lexpos):
        """ Find the column according to the lexpos.
        """
        last_cr = self._current_input.rfind('\n', 0, lexpos)
        if last_cr < 0:
            last_cr = 0
        column = lexpos - last_cr
        return column

    def input(self, input):
        if sys.version_info[0] >= 3:
            if isinstance(input, bytes):
                input = input.decode(self._encoding)
        elif isinstance(input, str):
            input = input.decode(self._encoding)
        self._current_input = input
        return self._lexer.input(input)

    def __getattr__(self, name):
        attr = getattr(self._lexer, name)
        if attr is None:
            raise AttributeError("'%s' object has no attribute '%s'" % (self, name))
        else:
            return attr
        return


class ConfitureParser(object):
    """ Parser for the Confiture format.
    """
    tokens = ConfitureLexer.tokens

    def __init__(self, input, **kwargs):
        self._input = input
        self._input_name = kwargs.pop('input_name', '<unknown>')
        self._external_opener = kwargs.pop('external_opener', default_external_opener)
        self._lexer = kwargs.pop('lexer', ConfitureLexer(input_name=self._input_name))
        self._parser = yacc.yacc(module=self, **kwargs)
        self._old_line = 0

    def _check_line(self, current, lineno, pos, token):
        if self._old_line == current:
            pos = Position(self._input_name, lineno, pos)
            raise ParsingError('Syntax error near of "%s", newline missing?' % token, pos)
        else:
            self._old_line = current

    start = 'top'

    def p_top(self, p):
        """top : section_content"""
        section = ConfigSection('__top__')
        for child in p[1]:
            if isinstance(child, ConfigSection):
                child.parent = section
            section.register(child)

        p[0] = section

    def p_assignation(self, p):
        """assignment : NAME ASSIGN value
                      | NAME ASSIGN list"""
        position = Position(self._input_name, p.lineno(3), p.lexer.column(p.lexpos(3)))
        value = ConfigValue(p[1], p[3], position=position)
        p[0] = value

    def p_value(self, p):
        """value : TEXT
                 | YES
                 | NO
                 | number"""
        p[0] = p[1]

    def p_number(self, p):
        """number : NUMBER
                  | NUMBER UNIT"""
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = p[1] * p[2]

    def p_list(self, p):
        """list : value LIST_SEP list_next
                | value LIST_SEP"""
        if len(p) == 3:
            p[0] = [
             p[1]]
        elif len(p) == 4:
            p[3].insert(0, p[1])
            p[0] = p[3]

    def p_list_next(self, p):
        """list_next : value
                     | value LIST_SEP
                     | value LIST_SEP list_next"""
        if len(p) in (2, 3):
            p[0] = [
             p[1]]
        elif len(p) == 4:
            p[3].insert(0, p[1])
            p[0] = p[3]

    def p_section_content_empty(self, p):
        """section_content : empty"""
        p[0] = []

    def p_section_content_assignation(self, p):
        """section_content : section_content assignment
                           | section_content section"""
        self._check_line(p.lexer.lineno, p.lineno(2), self._lexer.column(p.lexpos(2)), p[2].name)
        p[1].append(p[2])
        p[0] = p[1]

    def p_section_content_include(self, p):
        """section_content : section_content INCLUDE TEXT"""
        for external in self._external_opener(p[3]):
            p[1] += list(external.iterflatchildren())

        p[0] = p[1]

    def p_section(self, p):
        """section : NAME LBRACE section_content RBRACE
                   | NAME section_args LBRACE section_content RBRACE"""
        name = p[1]
        if len(p) == 5:
            args = None
            section_content = p[3]
        else:
            args = p[2]
            section_content = p[4]
        column = p.lexer.column(p.lexpos(1))
        position = Position(self._input_name, p.lineno(1), column)
        section = ConfigSection(name, args=args, position=position)
        for child in section_content:
            if isinstance(child, ConfigSection):
                child.parent = section
            section.register(child)

        p[0] = section
        return

    def p_section_args(self, p):
        """section_args : value LIST_SEP section_args
                        | value"""
        if len(p) == 2:
            position = Position(self._input_name, p.lineno(1), p.lexer.column(p.lexpos(1)))
            p[0] = ConfigValue('<args>', [p[1]], position=position)
        else:
            p[3].value.insert(0, p[1])
            p[0] = p[3]

    def p_empty(self, p):
        """empty :"""
        pass

    def p_error(self, token):
        if token is None:
            raise ParsingError('Unexpected end of file')
        column = self._lexer.column(token.lexpos)
        pos = Position(self._input_name, token.lineno, column)
        raise ParsingError('Syntax error near of "%s"' % token.value, pos)
        return

    def parse(self):
        return self._parser.parse(self._input, self._lexer, tracking=True)

    def __getattr__(self, name):
        attr = getattr(self._parser, name)
        if attr is None:
            raise AttributeError("'%s' object has no attribute '%s'" % (self, name))
        else:
            return attr
        return