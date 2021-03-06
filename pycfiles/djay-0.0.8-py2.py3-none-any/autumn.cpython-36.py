# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/Pygments/pygments/styles/autumn.py
# Compiled at: 2019-07-30 18:47:12
# Size of source mod 2**32: 2144 bytes
"""
    pygments.styles.autumn
    ~~~~~~~~~~~~~~~~~~~~~~

    A colorful style, inspired by the terminal highlighting style.

    :copyright: Copyright 2006-2019 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
from pygments.style import Style
from pygments.token import Keyword, Name, Comment, String, Error, Number, Operator, Generic, Whitespace

class AutumnStyle(Style):
    __doc__ = '\n    A colorful style, inspired by the terminal highlighting style.\n    '
    default_style = ''
    styles = {Whitespace: '#bbbbbb', 
     Comment: 'italic #aaaaaa', 
     Comment.Preproc: 'noitalic #4c8317', 
     Comment.Special: 'italic #0000aa', 
     Keyword: '#0000aa', 
     Keyword.Type: '#00aaaa', 
     Operator.Word: '#0000aa', 
     Name.Builtin: '#00aaaa', 
     Name.Function: '#00aa00', 
     Name.Class: 'underline #00aa00', 
     Name.Namespace: 'underline #00aaaa', 
     Name.Variable: '#aa0000', 
     Name.Constant: '#aa0000', 
     Name.Entity: 'bold #800', 
     Name.Attribute: '#1e90ff', 
     Name.Tag: 'bold #1e90ff', 
     Name.Decorator: '#888888', 
     String: '#aa5500', 
     String.Symbol: '#0000aa', 
     String.Regex: '#009999', 
     Number: '#009999', 
     Generic.Heading: 'bold #000080', 
     Generic.Subheading: 'bold #800080', 
     Generic.Deleted: '#aa0000', 
     Generic.Inserted: '#00aa00', 
     Generic.Error: '#aa0000', 
     Generic.Emph: 'italic', 
     Generic.Strong: 'bold', 
     Generic.Prompt: '#555555', 
     Generic.Output: '#888888', 
     Generic.Traceback: '#aa0000', 
     Error: '#F00 bg:#FAA'}