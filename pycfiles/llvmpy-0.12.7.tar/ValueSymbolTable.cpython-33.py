# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./src/ValueSymbolTable.py
# Compiled at: 2014-08-01 13:34:49
# Size of source mod 2**32: 486 bytes
from binding import *
from .Value import ValueSymbolTable, Value
from .ADT.StringRef import StringRef

@ValueSymbolTable
class ValueSymbolTable:
    if LLVM_VERSION >= (3, 3):
        _include_ = 'llvm/IR/ValueSymbolTable.h'
    else:
        _include_ = 'llvm/ValueSymbolTable.h'
    new = Constructor()
    delete = Destructor()
    lookup = Method(ptr(Value), cast(str, StringRef))
    empty = Method(cast(Bool, bool))
    size = Method(cast(Unsigned, int))
    dump = Method(Void)