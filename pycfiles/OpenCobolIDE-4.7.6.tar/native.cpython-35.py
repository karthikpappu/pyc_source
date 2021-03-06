# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-jqog4noo/pygments/pygments/styles/native.py
# Compiled at: 2016-12-29 05:31:34
# Size of source mod 2**32: 1938 bytes
"""
    pygments.styles.native
    ~~~~~~~~~~~~~~~~~~~~~~

    pygments version of my "native" vim theme.

    :copyright: Copyright 2006-2015 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
from pygments.style import Style
from pygments.token import Keyword, Name, Comment, String, Error, Number, Operator, Generic, Token, Whitespace

class NativeStyle(Style):
    __doc__ = '\n    Pygments version of the "native" vim theme.\n    '
    background_color = '#202020'
    highlight_color = '#404040'
    styles = {Token: '#d0d0d0', 
     Whitespace: '#666666', 
     Comment: 'italic #999999', 
     Comment.Preproc: 'noitalic bold #cd2828', 
     Comment.Special: 'noitalic bold #e50808 bg:#520000', 
     Keyword: 'bold #6ab825', 
     Keyword.Pseudo: 'nobold', 
     Operator.Word: 'bold #6ab825', 
     String: '#ed9d13', 
     String.Other: '#ffa500', 
     Number: '#3677a9', 
     Name.Builtin: '#24909d', 
     Name.Variable: '#40ffff', 
     Name.Constant: '#40ffff', 
     Name.Class: 'underline #447fcf', 
     Name.Function: '#447fcf', 
     Name.Namespace: 'underline #447fcf', 
     Name.Exception: '#bbbbbb', 
     Name.Tag: 'bold #6ab825', 
     Name.Attribute: '#bbbbbb', 
     Name.Decorator: '#ffa500', 
     Generic.Heading: 'bold #ffffff', 
     Generic.Subheading: 'underline #ffffff', 
     Generic.Deleted: '#d22323', 
     Generic.Inserted: '#589819', 
     Generic.Error: '#d22323', 
     Generic.Emph: 'italic', 
     Generic.Strong: 'bold', 
     Generic.Prompt: '#aaaaaa', 
     Generic.Output: '#cccccc', 
     Generic.Traceback: '#d22323', 
     Error: 'bg:#e3d2d2 #a61717'}