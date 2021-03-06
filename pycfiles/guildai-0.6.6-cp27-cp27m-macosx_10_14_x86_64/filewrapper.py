# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./guild/external/pip/_vendor/cachecontrol/filewrapper.py
# Compiled at: 2019-09-10 15:18:29
from io import BytesIO

class CallbackFileWrapper(object):
    """
    Small wrapper around a fp object which will tee everything read into a
    buffer, and when that file is closed it will execute a callback with the
    contents of that buffer.

    All attributes are proxied to the underlying file object.

    This class uses members with a double underscore (__) leading prefix so as
    not to accidentally shadow an attribute.
    """

    def __init__(self, fp, callback):
        self.__buf = BytesIO()
        self.__fp = fp
        self.__callback = callback

    def __getattr__(self, name):
        fp = self.__getattribute__('_CallbackFileWrapper__fp')
        return getattr(fp, name)

    def __is_fp_closed(self):
        try:
            return self.__fp.fp is None
        except AttributeError:
            pass

        try:
            return self.__fp.closed
        except AttributeError:
            pass

        return False

    def _close(self):
        if self.__callback:
            self.__callback(self.__buf.getvalue())
        self.__callback = None
        return

    def read(self, amt=None):
        data = self.__fp.read(amt)
        self.__buf.write(data)
        if self.__is_fp_closed():
            self._close()
        return data

    def _safe_read(self, amt):
        data = self.__fp._safe_read(amt)
        if amt == 2 and data == '\r\n':
            return data
        self.__buf.write(data)
        if self.__is_fp_closed():
            self._close()
        return data