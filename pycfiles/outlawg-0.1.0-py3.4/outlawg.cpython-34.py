# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/outlawg/outlawg.py
# Compiled at: 2016-05-05 00:56:11
# Size of source mod 2**32: 1519 bytes
"""Module for simple logging with focus on output readability."""
LINE_XLONG = 80
LINE_LONG = 70
LINE_MEDIUM = 40
LINE_SHORT = 20
ASTERISK = '*'
DBL_BAR = '='
DASH = '-'
DOT = '.'

class Outlawg(object):

    def __init__(self):
        pass

    def label_format(self, label, header_line=''):
        return '\n{0}\n{1}\n{2}\n'.format(header_line, label, header_line)

    def header_line(self, size='M', line_char=None):
        if size == 'XL':
            line_char = line_char if line_char else ASTERISK
            return line_char * LINE_XLONG
        else:
            if size == 'L':
                line_char = line_char if line_char else DBL_BAR
                return line_char * LINE_LONG
            if size == 'M':
                line_char = line_char if line_char else DASH
                return line_char * LINE_MEDIUM
            if size == 'S':
                line_char = line_char if line_char else DOT
                return line_char * LINE_SHORT
            return DASH * LINE_MEDIUM

    def header(self, label, size='M', line_char=''):
        print(self.label_format(label, self.header_line(size, line_char)))

    def subheader(self, label):
        print('\n{0}\n'.format(label.upper()))

    def banner(self, label, line_length=LINE_SHORT, label_char='*'):
        header_line = self.header_line('S', '*')
        header_line = '{0}\n{0}\n{0}\n{0}\n{0}'.format(header_line)
        print('{1}\n{0}\n{1}\n'.format(label.upper(), header_line))


if __name__ == '__main__':
    log = Outlawg()
    log.header('HEY')