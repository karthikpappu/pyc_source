# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/py/py/_io/terminalwriter.py
# Compiled at: 2019-07-30 18:47:10
# Size of source mod 2**32: 14660 bytes
"""

Helper functions for writing to terminals and files.

"""
import sys, os, unicodedata, py
py3k = sys.version_info[0] >= 3
py33 = sys.version_info >= (3, 3)
from py.builtin import text, bytes
win32_and_ctypes = False
colorama = None
if sys.platform == 'win32':
    try:
        import colorama
    except ImportError:
        try:
            import ctypes
            win32_and_ctypes = True
        except ImportError:
            pass

def _getdimensions():
    if py33:
        import shutil
        size = shutil.get_terminal_size()
        return (
         size.lines, size.columns)
    else:
        import termios, fcntl, struct
        call = fcntl.ioctl(1, termios.TIOCGWINSZ, '\x00\x00\x00\x00\x00\x00\x00\x00')
        height, width = struct.unpack('hhhh', call)[:2]
        return (height, width)


def get_terminal_width():
    width = 0
    try:
        _, width = _getdimensions()
    except py.builtin._sysex:
        raise
    except:
        pass

    if width == 0:
        width = int(os.environ.get('COLUMNS', 80))
    if width < 40:
        width = 80
    return width


terminal_width = get_terminal_width()
char_width = {'A':1, 
 'F':2, 
 'H':1, 
 'N':1, 
 'Na':1, 
 'W':2}

def get_line_width(text):
    text = unicodedata.normalize('NFC', text)
    return sum(char_width.get(unicodedata.east_asian_width(c), 1) for c in text)


def ansi_print(text, esc, file=None, newline=True, flush=False):
    if file is None:
        file = sys.stderr
    else:
        text = text.rstrip()
        if esc:
            if not isinstance(esc, tuple):
                esc = (
                 esc,)
        if esc:
            if sys.platform != 'win32':
                if file.isatty():
                    text = ''.join(['\x1b[%sm' % cod for cod in esc]) + text + '\x1b[0m'
        if newline:
            text += '\n'
        if esc and win32_and_ctypes and file.isatty():
            if 1 in esc:
                bold = True
                esc = tuple([x for x in esc if x != 1])
            else:
                bold = False
            esctable = {(): FOREGROUND_WHITE, (31, ): FOREGROUND_RED, 
             (32, ): FOREGROUND_GREEN, 
             (33, ): FOREGROUND_GREEN | FOREGROUND_RED, 
             (34, ): FOREGROUND_BLUE, 
             (35, ): FOREGROUND_BLUE | FOREGROUND_RED, 
             (36, ): FOREGROUND_BLUE | FOREGROUND_GREEN, 
             (37, ): FOREGROUND_WHITE, 
             (39, ): FOREGROUND_WHITE}
            attr = esctable.get(esc, FOREGROUND_WHITE)
            if bold:
                attr |= FOREGROUND_INTENSITY
            STD_OUTPUT_HANDLE = -11
            STD_ERROR_HANDLE = -12
            if file is sys.stderr:
                handle = GetStdHandle(STD_ERROR_HANDLE)
            else:
                handle = GetStdHandle(STD_OUTPUT_HANDLE)
            oldcolors = GetConsoleInfo(handle).wAttributes
            attr |= oldcolors & 240
            SetConsoleTextAttribute(handle, attr)
            while len(text) > 32768:
                file.write(text[:32768])
                text = text[32768:]

            if text:
                file.write(text)
            SetConsoleTextAttribute(handle, oldcolors)
        else:
            file.write(text)
        if flush:
            file.flush()


def should_do_markup(file):
    if os.environ.get('PY_COLORS') == '1':
        return True
    else:
        if os.environ.get('PY_COLORS') == '0':
            return False
        return hasattr(file, 'isatty') and file.isatty() and os.environ.get('TERM') != 'dumb' and not (sys.platform.startswith('java') and os._name == 'nt')


class TerminalWriter(object):
    _esctable = dict(black=30, red=31, green=32, yellow=33, blue=34,
      purple=35,
      cyan=36,
      white=37,
      Black=40,
      Red=41,
      Green=42,
      Yellow=43,
      Blue=44,
      Purple=45,
      Cyan=46,
      White=47,
      bold=1,
      light=2,
      blink=5,
      invert=7)

    def __init__(self, file=None, stringio=False, encoding=None):
        if file is None:
            if stringio:
                self.stringio = file = py.io.TextIO()
            else:
                from sys import stdout as file
        else:
            if py.builtin.callable(file):
                if not (hasattr(file, 'write') and hasattr(file, 'flush')):
                    file = WriteFile(file, encoding=encoding)
        if hasattr(file, 'isatty'):
            if file.isatty():
                if colorama:
                    file = colorama.AnsiToWin32(file).stream
        self.encoding = encoding or getattr(file, 'encoding', 'utf-8')
        self._file = file
        self.hasmarkup = should_do_markup(file)
        self._lastlen = 0
        self._chars_on_current_line = 0
        self._width_of_current_line = 0

    @property
    def fullwidth(self):
        if hasattr(self, '_terminal_width'):
            return self._terminal_width
        else:
            return get_terminal_width()

    @fullwidth.setter
    def fullwidth(self, value):
        self._terminal_width = value

    @property
    def chars_on_current_line(self):
        """Return the number of characters written so far in the current line.

        Please note that this count does not produce correct results after a reline() call,
        see #164.

        .. versionadded:: 1.5.0

        :rtype: int
        """
        return self._chars_on_current_line

    @property
    def width_of_current_line(self):
        """Return an estimate of the width so far in the current line.

        .. versionadded:: 1.6.0

        :rtype: int
        """
        return self._width_of_current_line

    def _escaped(self, text, esc):
        if esc:
            if self.hasmarkup:
                text = ''.join(['\x1b[%sm' % cod for cod in esc]) + text + '\x1b[0m'
        return text

    def markup(self, text, **kw):
        esc = []
        for name in kw:
            if name not in self._esctable:
                raise ValueError('unknown markup: %r' % (name,))
            if kw[name]:
                esc.append(self._esctable[name])

        return self._escaped(text, tuple(esc))

    def sep(self, sepchar, title=None, fullwidth=None, **kw):
        if fullwidth is None:
            fullwidth = self.fullwidth
        else:
            if sys.platform == 'win32':
                fullwidth -= 1
            else:
                if title is not None:
                    N = max((fullwidth - len(title) - 2) // (2 * len(sepchar)), 1)
                    fill = sepchar * N
                    line = '%s %s %s' % (fill, title, fill)
                else:
                    line = sepchar * (fullwidth // len(sepchar))
            if len(line) + len(sepchar.rstrip()) <= fullwidth:
                line += sepchar.rstrip()
        (self.line)(line, **kw)

    def write(self, msg, **kw):
        if msg:
            if not isinstance(msg, (bytes, text)):
                msg = text(msg)
            else:
                self._update_chars_on_current_line(msg)
                if self.hasmarkup:
                    if kw:
                        markupmsg = (self.markup)(msg, **kw)
                markupmsg = msg
            write_out(self._file, markupmsg)

    def _update_chars_on_current_line(self, text_or_bytes):
        newline = b'\n' if isinstance(text_or_bytes, bytes) else '\n'
        current_line = text_or_bytes.rsplit(newline, 1)[(-1)]
        if isinstance(current_line, bytes):
            current_line = current_line.decode('utf-8', errors='replace')
        else:
            if newline in text_or_bytes:
                self._chars_on_current_line = len(current_line)
                self._width_of_current_line = get_line_width(current_line)
            else:
                self._chars_on_current_line += len(current_line)
                self._width_of_current_line += get_line_width(current_line)

    def line(self, s='', **kw):
        (self.write)(s, **kw)
        self._checkfill(s)
        self.write('\n')

    def reline(self, line, **kw):
        if not self.hasmarkup:
            raise ValueError('cannot use rewrite-line without terminal')
        (self.write)(line, **kw)
        self._checkfill(line)
        self.write('\r')
        self._lastlen = len(line)

    def _checkfill(self, line):
        diff2last = self._lastlen - len(line)
        if diff2last > 0:
            self.write(' ' * diff2last)


class Win32ConsoleWriter(TerminalWriter):

    def write(self, msg, **kw):
        if msg:
            if not isinstance(msg, (bytes, text)):
                msg = text(msg)
            else:
                self._update_chars_on_current_line(msg)
                oldcolors = None
                if self.hasmarkup:
                    if kw:
                        handle = GetStdHandle(STD_OUTPUT_HANDLE)
                        oldcolors = GetConsoleInfo(handle).wAttributes
                        default_bg = oldcolors & 240
                        attr = default_bg
                        if kw.pop('bold', False):
                            attr |= FOREGROUND_INTENSITY
                        if kw.pop('red', False):
                            attr |= FOREGROUND_RED
                        else:
                            if kw.pop('blue', False):
                                attr |= FOREGROUND_BLUE
                            else:
                                if kw.pop('green', False):
                                    attr |= FOREGROUND_GREEN
                                else:
                                    if kw.pop('yellow', False):
                                        attr |= FOREGROUND_GREEN | FOREGROUND_RED
                                    else:
                                        attr |= oldcolors & 7
                            SetConsoleTextAttribute(handle, attr)
                write_out(self._file, msg)
                if oldcolors:
                    SetConsoleTextAttribute(handle, oldcolors)


class WriteFile(object):

    def __init__(self, writemethod, encoding=None):
        self.encoding = encoding
        self._writemethod = writemethod

    def write(self, data):
        if self.encoding:
            data = data.encode(self.encoding, 'replace')
        self._writemethod(data)

    def flush(self):
        pass


if win32_and_ctypes:
    TerminalWriter = Win32ConsoleWriter
    import ctypes
    from ctypes import wintypes
    STD_OUTPUT_HANDLE = -11
    STD_ERROR_HANDLE = -12
    FOREGROUND_BLACK = 0
    FOREGROUND_BLUE = 1
    FOREGROUND_GREEN = 2
    FOREGROUND_RED = 4
    FOREGROUND_WHITE = 7
    FOREGROUND_INTENSITY = 8
    BACKGROUND_BLACK = 0
    BACKGROUND_BLUE = 16
    BACKGROUND_GREEN = 32
    BACKGROUND_RED = 64
    BACKGROUND_WHITE = 112
    BACKGROUND_INTENSITY = 128
    SHORT = ctypes.c_short

    class COORD(ctypes.Structure):
        _fields_ = [
         (
          'X', SHORT),
         (
          'Y', SHORT)]


    class SMALL_RECT(ctypes.Structure):
        _fields_ = [
         (
          'Left', SHORT),
         (
          'Top', SHORT),
         (
          'Right', SHORT),
         (
          'Bottom', SHORT)]


    class CONSOLE_SCREEN_BUFFER_INFO(ctypes.Structure):
        _fields_ = [
         (
          'dwSize', COORD),
         (
          'dwCursorPosition', COORD),
         (
          'wAttributes', wintypes.WORD),
         (
          'srWindow', SMALL_RECT),
         (
          'dwMaximumWindowSize', COORD)]


    _GetStdHandle = ctypes.windll.kernel32.GetStdHandle
    _GetStdHandle.argtypes = [wintypes.DWORD]
    _GetStdHandle.restype = wintypes.HANDLE

    def GetStdHandle(kind):
        return _GetStdHandle(kind)


    SetConsoleTextAttribute = ctypes.windll.kernel32.SetConsoleTextAttribute
    SetConsoleTextAttribute.argtypes = [wintypes.HANDLE, wintypes.WORD]
    SetConsoleTextAttribute.restype = wintypes.BOOL
    _GetConsoleScreenBufferInfo = ctypes.windll.kernel32.GetConsoleScreenBufferInfo
    _GetConsoleScreenBufferInfo.argtypes = [wintypes.HANDLE,
     ctypes.POINTER(CONSOLE_SCREEN_BUFFER_INFO)]
    _GetConsoleScreenBufferInfo.restype = wintypes.BOOL

    def GetConsoleInfo(handle):
        info = CONSOLE_SCREEN_BUFFER_INFO()
        _GetConsoleScreenBufferInfo(handle, ctypes.byref(info))
        return info


    def _getdimensions():
        handle = GetStdHandle(STD_OUTPUT_HANDLE)
        info = GetConsoleInfo(handle)
        return (
         info.dwSize.Y, info.dwSize.X - 1)


def write_out(fil, msg):
    try:
        fil.write(msg)
    except UnicodeEncodeError:
        if fil.encoding:
            try:
                fil.write(msg.encode(fil.encoding))
            except UnicodeEncodeError:
                pass
            else:
                fil.flush()
                return
        msg = msg.encode('unicode-escape').decode('ascii')
        fil.write(msg)

    fil.flush()