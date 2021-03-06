# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/py_lex_java/__init__.py
# Compiled at: 2017-07-11 13:32:45
# Size of source mod 2**32: 771 bytes
import os
from . import _py_lex_java
__dir__ = os.path.abspath(os.path.dirname(__file__))

class JavaError(Exception):

    def getJavaException(self):
        return self.args[0]

    def __str__(self):
        writer = StringWriter()
        self.getJavaException().printStackTrace(PrintWriter(writer))
        return '\n'.join((unicode(super(JavaError, self)), '    Java stacktrace:', unicode(writer)))


class InvalidArgsError(Exception):
    pass


_py_lex_java._set_exception_types(JavaError, InvalidArgsError)
VERSION = '1.8.0'
CLASSPATH = [os.path.join(__dir__, 'lex-java-1.0-SNAPSHOT-jar-with-dependencies.jar')]
CLASSPATH = os.pathsep.join(CLASSPATH)
_py_lex_java.CLASSPATH = CLASSPATH
_py_lex_java._set_function_self(_py_lex_java.initVM, _py_lex_java)
from ._py_lex_java import *