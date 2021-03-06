# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/Pygments/pygments/styles/trac.py
# Compiled at: 2019-07-30 18:47:12
# Size of source mod 2**32: 1933 bytes
"""
    pygments.styles.trac
    ~~~~~~~~~~~~~~~~~~~~

    Port of the default trac highlighter design.

    :copyright: Copyright 2006-2019 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
from pygments.style import Style
from pygments.token import Keyword, Name, Comment, String, Error, Number, Operator, Generic, Whitespace

class TracStyle(Style):
    __doc__ = '\n    Port of the default trac highlighter design.\n    '
    default_style = ''
    styles = {Whitespace: '#bbbbbb', 
     Comment: 'italic #999988', 
     Comment.Preproc: 'bold noitalic #999999', 
     Comment.Special: 'bold #999999', 
     Operator: 'bold', 
     String: '#bb8844', 
     String.Regex: '#808000', 
     Number: '#009999', 
     Keyword: 'bold', 
     Keyword.Type: '#445588', 
     Name.Builtin: '#999999', 
     Name.Function: 'bold #990000', 
     Name.Class: 'bold #445588', 
     Name.Exception: 'bold #990000', 
     Name.Namespace: '#555555', 
     Name.Variable: '#008080', 
     Name.Constant: '#008080', 
     Name.Tag: '#000080', 
     Name.Attribute: '#008080', 
     Name.Entity: '#800080', 
     Generic.Heading: '#999999', 
     Generic.Subheading: '#aaaaaa', 
     Generic.Deleted: 'bg:#ffdddd #000000', 
     Generic.Inserted: 'bg:#ddffdd #000000', 
     Generic.Error: '#aa0000', 
     Generic.Emph: 'italic', 
     Generic.Strong: 'bold', 
     Generic.Prompt: '#555555', 
     Generic.Output: '#888888', 
     Generic.Traceback: '#aa0000', 
     Error: 'bg:#e3d2d2 #a61717'}