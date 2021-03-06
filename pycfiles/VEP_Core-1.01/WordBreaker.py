# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\LocalUsers\ealexand\VEP_Core\vep_core\Ity\Tokenizers\WordTokenizer\WordBreaker.py
# Compiled at: 2013-12-05 13:11:49
"""
Heads up: this is a refactored version of gleicher's WordBreaker.

Instead of returning strings, it returns dictionaries containing "word" and "startPos" keys.

Docucscope Jr - the Naive Way!

Utilities for breaking texts into words. based on lots of assumptions.

Note: The WordBreaker creates an iterator that lets you loop over the words in
a string. At present, there is no real way to connect it to a file, so you have
to read in the whole text.

This makes a vain attempt to mimic Docuscope's word breaking rules, which 
may be a bit problematic. dashes are always part of words. single quotes are
part of words, except at the beginning and end

TODO:
    - Make WordBreaker work from a file without reading the whole text
    - Be smarter about quotes
    - Be smarter about punctuation
    - Deal with the mysteries of weird characters

Created on Sun Nov 27 11:46:49 2011

@author: gleicher
"""
import string

def myisspace(c):
    if c == ' ' or c == '\t':
        return True
    return False


def validletter(c):
    return c.isalnum() or c == '-' or c == "'"


class WordBreaker:
    """class for breaking a string into a sequence of words"""

    def __init__(self, _str):
        """create a WordBreaker for a given string"""
        self.str = _str
        self.strl = len(_str)
        self.pos = 0

    def __iter__(self):
        """this is required so that python knows that it can be iterated over"""
        return self

    def peek(self):
        """return the current character. if it's something weird, then advance"""
        c = self.str[self.pos]
        if c == '|' or c == '_' or ord(c) > 127:
            self.pos = self.pos + 1
            return self.peek()
        return c

    def unpeek(self, char):
        """put the character back (or at least try) - no error checking!"""
        if self.pos > 0:
            self.pos -= 1

    def getchar(self):
        c = self.peek()
        self.pos = self.pos + 1
        return c

    def next(self):
        """This is the main thing that does the iteration"""
        if self.pos >= self.strl:
            raise StopIteration
        strc = []
        try:
            while myisspace(self.peek()):
                self.pos = self.pos + 1

            c = self.getchar()
            strc.append(c)
            if c == '\n' or c == '\r':
                while self.peek() == c:
                    self.pos = self.pos + 1

                return [['\n'], self.pos - 1, 1]
            if c == '&':
                try:
                    for i in range(8):
                        if self.str[(self.pos + i)] == ';':
                            raise KeyError

                except KeyError:
                    while c != ';':
                        c = self.getchar()
                        strc.append(c)

                    return [
                     [
                      ('').join(strc)], self.pos - len(strc), len(strc)]
                except IndexError:
                    pass

                return [
                 [
                  '&'], self.pos - 1, 1]
            if c in string.punctuation and c != '-':
                while self.peek() == c:
                    self.pos = self.pos + 1
                    strc.append(c)

                return [[('').join(strc)], self.pos - len(strc), len(strc)]
            c = self.peek()
            while validletter(c):
                strc.append(c)
                self.pos += 1
                c = self.peek()

            if strc[(-1)] == "'":
                strc.pop()
                self.unpeek("'")
            return [
             [
              ('').join(strc).lower()], self.pos - len(strc), len(strc)]
        except IndexError:
            if len(strc) > 0:
                self.pos = self.strl
                return [
                 [
                  ('').join(strc)], self.pos - len(strc), len(strc)]
            raise StopIteration