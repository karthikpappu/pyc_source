# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: bin/../mmseg/__init__.py
# Compiled at: 2013-02-10 18:42:51
import os
from _mmseg import Dictionary as _Dictionary, Token, Algorithm

class Dictionary(_Dictionary):
    dictionaries = (
     (
      'chars', os.path.join(os.path.dirname(__file__), 'data', 'chars.dic')),
     (
      'words', os.path.join(os.path.dirname(__file__), 'data', 'words.dic')))

    @staticmethod
    def load_dictionaries():
        for t, d in Dictionary.dictionaries:
            if t == 'chars':
                if not Dictionary.load_chars(d):
                    raise IOError("Cannot open '%s'" % d)
            elif t == 'words':
                if not Dictionary.load_words(d):
                    raise IOError("Cannot open '%s'" % d)


dict_load_defaults = Dictionary.load_dictionaries