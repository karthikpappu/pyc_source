# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyBabyMaker/parse.py
# Compiled at: 2020-05-01 05:18:06
# Size of source mod 2**32: 1056 bytes
__doc__ = '\nThis module provides limited functionality to extract variables from certain\ntype of C++ expressions.\n\nCurrently, supported C++ expressions includes arithmetic and boolean calculation\nand nested function calls.\n'
import re

def is_numeral--- This code section failed: ---

 L.  21         0  SETUP_FINALLY        16  'to 16'

 L.  22         2  LOAD_GLOBAL              float
                4  LOAD_FAST                'n'
                6  CALL_FUNCTION_1       1  ''
                8  POP_TOP          

 L.  23        10  POP_BLOCK        
               12  LOAD_CONST               True
               14  RETURN_VALUE     
             16_0  COME_FROM_FINALLY     0  '0'

 L.  24        16  DUP_TOP          
               18  LOAD_GLOBAL              ValueError
               20  COMPARE_OP               exception-match
               22  POP_JUMP_IF_FALSE    36  'to 36'
               24  POP_TOP          
               26  POP_TOP          
               28  POP_TOP          

 L.  25        30  POP_EXCEPT       
               32  LOAD_CONST               False
               34  RETURN_VALUE     
             36_0  COME_FROM            22  '22'
               36  END_FINALLY      

Parse error at or near `RETURN_VALUE' instruction at offset 14


def find_all_args(s, tokens=[
 '[\\w\\d_]*\\(', '\\)', ',',
 '\\+', '-', '\\*', '/', '%',
 '&&', '\\|\\|',
 '!', '>', '<', '=']):
    """
    Find all arguments inside a C++ expression ``s``.
    """
    for t in tokens:
        s = re.sub(t, ' ', s)

    return s.split()


def find_all_vars(s, **kwargs):
    """
    Find all arguments, minus numerals, inside a C++ expression ``s``.
    """
    args = find_all_args(s, **kwargs)
    return [v for v in args if not is_numeral(v)]