# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Ft\Lib\DistExt\Formatters\XmlFormatter.py
# Compiled at: 2006-08-12 10:56:26
import pydoc, cStringIO
from repr import Repr

class XmlRepr(pydoc.TextRepr):
    """
    Class for safely making a XML representation of a Python object.
    """
    __module__ = __name__
    _escape_table = [
     (
      '&', '&amp;'), ('<', '&lt;'), ('>', '&gt;'), ('"', '&quot;')]

    def escape(self, text):
        for (char, repl) in self._escape_table:
            text = text.replace(char, repl)

        return text

    def repr(self, object):
        return self.escape(pydoc.TextRepr.repr(self, object))

    repr_unicode = repr_str = pydoc.TextRepr.repr_string


class XmlFormatter(XmlRepr):
    __module__ = __name__
    indent = '  '
    document_type = None

    def __init__(self, dist_command):
        XmlRepr.__init__(self)
        self.dist_command = dist_command
        self.module = None
        self.write = None
        self.indent_level = 0
        return
        return

    def warn(self, msg):
        return self.dist_command.warn(msg)

    def start_element(self, tagname, attributes={}):
        self.write(self.indent * self.indent_level)
        self.write('<%s' % tagname)
        for (name, value) in attributes.items():
            self.write(' %s="%s"' % (name, self.escape(str(value))))

        self.write('>\n')
        self.indent_level += 1
        return

    def end_element(self, tagname):
        self.indent_level -= 1
        self.write(self.indent * self.indent_level)
        self.write('</%s>\n' % tagname)
        return

    def write_element(self, tagname, attributes={}, content=''):
        self.write(self.indent * self.indent_level)
        self.write('<%s' % tagname)
        for (name, value) in attributes.items():
            self.write(' %s="%s"' % (name, self.escape(str(value))))

        if content:
            self.write('>%s</%s>\n' % (content, tagname))
        else:
            self.write('/>\n')
        return

    def section(self, title, list, format):
        self.start_element(title)
        for (name, object) in list:
            format(object, name)

        self.end_element(title)
        return

    def format(self, object, stream, encoding=None):
        """
        Print documentation for a Python object to a stream.
        """
        self.module = object
        self.write = stream.write
        self.indent_level = 0
        self.write('<?xml version="1.0"')
        if encoding:
            self.write(' encoding="%s"' % encoding)
        self.write('?>\n')
        if self.document_type and not isinstance(object, self.document_type):
            expected = self.document_type.__name__
            compared = object is None and 'None' or type(object).__name__
            raise TypeError('argument must be %s, not %s' % (expected, compared))
        self.document(object)
        return
        return

    def document(self, object):
        raise NotImplementedError('subclass %s must override' % self.__class__)