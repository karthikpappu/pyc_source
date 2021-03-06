# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\lib\CDictExpressParse.py
# Compiled at: 2018-09-23 11:16:03
from lib.ExpressToken import lexer

class CDictExpressParse:

    def __init__(self):
        pass

    def get(self, dc, exp):
        lttok = []
        lexer.input(exp)
        while True:
            tok = lexer.token()
            if not tok:
                break
            lttok.append(tok)

        node = dc
        blist = False
        for tok in lttok:
            if tok.type == 'ID':
                name = tok.value
                node = node[name]
            elif tok.type == 'PERIOD':
                pass
            elif tok.type == 'LBRACKET':
                blist = True
            elif tok.type == 'RBRACKET':
                blist = False
            elif tok.type == 'VAL_INTEGER':
                if blist == True:
                    name = int(tok.value)
                    node = node[name]
                else:
                    name = tok.value
                    node = node[name]
                    continue

        val = node
        return val

    def set(self, dc, exp, val):
        lttok = []
        lexer.input(exp)
        while True:
            tok = lexer.token()
            if not tok:
                break
            lttok.append(tok)

        xpath = ''
        name = ''
        blist = False
        for tok in lttok:
            if tok.type == 'ID':
                name = tok.value
            elif tok.type == 'PERIOD':
                if name != '':
                    xpath += '["' + name + '"]'
                    name = ''
            elif tok.type == 'LBRACKET':
                if name != '':
                    xpath += '["' + name + '"]'
                    name = ''
                xpath += '['
                blist = True
            elif tok.type == 'RBRACKET':
                xpath += ']'
                name = ''
                blist = False
            elif tok.type == 'VAL_INTEGER':
                xpath += str(tok.value)

        if name != '':
            xpath += '["' + name + '"]'
            name = ''
        code = 'dc' + xpath + '=' + 'val'
        exec code
        return dc