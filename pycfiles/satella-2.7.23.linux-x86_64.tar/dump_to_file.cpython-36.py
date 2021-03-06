# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.6.7/lib/python3.6/site-packages/satella/exception_handling/dump_to_file.py
# Compiled at: 2020-05-08 08:03:23
# Size of source mod 2**32: 3956 bytes
from __future__ import print_function, absolute_import, division
import os, typing as tp, uuid
from satella.coding import silence_excs
from satella.instrumentation import Traceback
from .exception_handlers import BaseExceptionHandler
__all__ = [
 'DumpToFileHandler']
AsStreamTypeAccept = tp.Union[(str, tp.IO, None)]
AsStreamTypeAcceptHR = tp.Union[(str, tp.TextIO)]
AsStreamTypeAcceptIN = tp.Union[(str, tp.BinaryIO)]

class AsStream:
    MODE_FILE = 0
    MODE_STREAM = 1
    MODE_DEVNULL = 2
    __slots__ = ('o', 'human_readable', 'mode', 'file')

    def __init__(self, o: AsStreamTypeAccept, human_readable: bool):
        """
        A stream to dump to

        :param o: stream, or a file name to use, or None to use /dev/null
        :param human_readable: whether the output should be human-readable
            or a pickle (False for pickle)
        """
        self.o = o
        self.human_readable = human_readable
        if isinstance(o, str):
            if os.path.isdir(o):
                self.o = os.path.join(o, uuid.uuid4().hex)
            self.mode = AsStream.MODE_FILE
        else:
            if hasattr(o, 'write'):
                self.mode = AsStream.MODE_STREAM
            else:
                if o is None:
                    self.mode = AsStream.MODE_DEVNULL
                else:
                    raise TypeError('invalid stream object')

    def __enter__(self) -> tp.Union[(tp.TextIO, tp.BinaryIO)]:
        if self.mode == AsStream.MODE_FILE:
            self.file = open((self.o), ('w' if self.human_readable else 'wb'), encoding=('utf8' if self.human_readable else None))
            return self.file.__enter__()
        else:
            if self.mode == AsStream.MODE_STREAM:
                return self.o
            if self.mode == AsStream.MODE_DEVNULL:

                class NoopFile(object):

                    def write(self, v):
                        pass

                    def flush(self):
                        pass

                self.o = NoopFile()
                return self.o

    def __exit__(self, exc_type, exc_val, exc_tp):
        if self.mode == AsStream.MODE_FILE:
            return self.file.__exit__(exc_type, exc_val, exc_tp)
        if self.mode == AsStream.MODE_STREAM:
            with silence_excs(AttributeError):
                self.o.flush()
        if self.mode == AsStream.MODE_DEVNULL:
            pass


class DumpToFileHandler(BaseExceptionHandler):
    __doc__ = '\n    Write the stack trace to a stream-file.\n\n    Note that your file-like objects you throw into that must support only .write() and optionally\n    .flush()\n    '
    __slots__ = ('hr', 'tb')

    def __init__(self, human_readables, trace_pickles=None):
        """
        Handler that dumps an exception to a file.

        :param human_readables: iterable of either a file-like objects, or paths where
            human-readable files will be output
        :param trace_pickles: iterable of either a file-like objects, or paths where pickles with
            stack status will be output
        """
        super(DumpToFileHandler, self).__init__()
        self.hr = [AsStream(x, True) if not isinstance(x, AsStream) else x for x in human_readables]
        self.tb = [AsStream(x, False) if not isinstance(x, AsStream) else x for x in trace_pickles or []]

    def handle_exception(self, type_, value, traceback) -> bool:
        try:
            tb = Traceback()
        except ValueError:
            return False
        else:
            for q in self.hr:
                with q as (f):
                    f.write('Unhandled exception caught: \n')
                    tb.pretty_print(output=f)

            for q in self.tb:
                with q as (f):
                    f.write(tb.pickle())