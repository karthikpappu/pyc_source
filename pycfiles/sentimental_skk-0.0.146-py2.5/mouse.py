# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/sskk/canossa/canossa/mouse.py
# Compiled at: 2014-04-25 02:25:24
from stub import *
import time
from constant import *
_DOUBLE_CLICK_SPAN = 0.2

class IMouseMode:

    def setenabled(self, value):
        raise NotImplementedError('IMouseMode::setenabled')

    def getprotocol(self):
        raise NotImplementedError('IMouseMode::getprotocol')

    def setprotocol(self, protocol):
        raise NotImplementedError('IMouseMode::setprotocol')

    def getencoding(self):
        raise NotImplementedError('IMouseMode::getencoding')

    def setencoding(self, encoding):
        raise NotImplementedError('IMouseMode::getencoding')

    def getfocusmode(self):
        raise NotImplementedError('IMouseMode::getfocusmode')

    def setfocusmode(self, mode):
        raise NotImplementedError('IMouseMode::setfocusmode')


class IFocusListener:

    def onfocusin(self):
        raise NotImplementedError('IFocusListener::onfocusin')

    def onfocusout(self):
        raise NotImplementedError('IFocusListener::onfocusout')


class IMouseListener:

    def mouseenabled(self):
        raise NotImplementedError('IMouseListener::mouseenabled')

    def onmousedown(self, context, x, y):
        raise NotImplementedError('IMouseListener::onmousedown')

    def onmouseup(self, context, x, y):
        raise NotImplementedError('IMouseListener::onmouseup')

    def onclick(self, context, x, y):
        raise NotImplementedError('IMouseListener::onclick')

    def ondoubleclick(self, context, x, y):
        raise NotImplementedError('IMouseListener::ondoubleclick')

    def onmousehover(self, context, x, y):
        raise NotImplementedError('IMouseListener::onmousehover')

    def onscrolldown(self, context, x, y):
        raise NotImplementedError('IMouseListener::onscrolldown')

    def onscrollup(self, context, x, y):
        raise NotImplementedError('IMouseListener::onscrollup')

    def ondragstart(self, s, x, y):
        raise NotImplementedError('IMouseListener::ondragstart')

    def ondragend(self, s, x, y):
        raise NotImplementedError('IMouseListener::ondragend')

    def ondragmove(self, context, x, y):
        raise NotImplementedError('IMouseListener::ondragmove')


class IMouseModeImpl(IMouseMode):
    """
    >>> import StringIO
    >>> s = StringIO.StringIO()
    >>> mouse_mode = IMouseModeImpl()
    >>> mouse_mode.setenabled(s, True)
    >>> print s.getvalue().replace("\x1b", "<ESC>")
    <ESC>[?1000h<ESC>[?1002h<ESC>[?1003h<ESC>[?1004h<ESC>[?1015h<ESC>[?1006h
    >>> s.truncate(0)
    >>> mouse_mode.setenabled(s, False)
    >>> print s.getvalue().replace("\x1b", "<ESC>")
    <ESC>[?1000l<ESC>[?1004l
    >>> s.truncate(0)
    """
    _protocol = 0
    _encoding = 0
    _focusmode = 0

    def setenabled(self, s, value):
        if value:
            s.write('\x1b[?1000h')
            s.write('\x1b[?1002h')
            s.write('\x1b[?1003h')
            s.write('\x1b[?1004h')
            s.write('\x1b[?1015h')
            s.write('\x1b[?1006h')
        else:
            if self._protocol == 0:
                s.write('\x1b[?1000l')
            else:
                s.write('\x1b[?%dl' % self._protocol)
                if self._encoding != 0:
                    s.write('\x1b[?%dl' % self._encoding)
            if self._focusmode == 0:
                s.write('\x1b[?1004l')

    def getprotocol(self):
        return self._protocol

    def setprotocol(self, protocol):
        self._protocol = protocol

    def getencoding(self):
        return self._encoding

    def setencoding(self, encoding):
        self._encoding = encoding

    def getfocusmode(self):
        return self._focusmode

    def setfocusmode(self, mode):
        self._focusmode = mode


def _parse_params(params, minimum=0, offset=0, minarg=1):
    param = 0
    for c in params:
        if c < 58:
            param = param * 10 + c - 48
        elif c < 60:
            param += offset
            if minimum > param:
                yield minimum
            else:
                yield param
            minarg -= 1
            param = 0

    param += offset
    if minimum > param:
        yield minimum
    else:
        yield param
    minarg -= 1
    yield param
    if minarg > 0:
        yield minimum


class ModeHandler(tff.DefaultHandler, IMouseModeImpl):

    def __init__(self, listener, termprop):
        self._listener = listener
        self._termprop = termprop

    def handle_esc(self, context, intermediate, final):
        if final == 99 and not intermediate:
            self.setprotocol(0)
            self.setencoding(0)
            self.setfocusmode(0)
        return False

    def handle_csi(self, context, parameter, intermediate, final):
        if self._handle_mode(context, parameter, intermediate, final):
            return True
        if final == 114 and parameter:
            if parameter[0] == 60 and not intermediate:
                self._listener.notifyimerestore()
                return False
        elif final == 115 and parameter:
            if parameter[0] == 60 and not intermediate:
                self._listener.notifyimesave()
                return False
        elif final == 116 and parameter:
            if parameter[0] == 60 and not intermediate:
                length = len(parameter)
                if parameter == 1:
                    self._listener.notifyimeoff()
                elif parameter == 1 or parameter[2] == 59:
                    if parameter[1] == 48:
                        self._listener.notifyimeoff()
                    elif parameter[1] == 49:
                        self._listener.notifyimeon()
                return False
        return False

    def _handle_mode(self, context, parameter, intermediate, final):
        if len(parameter) >= 5:
            if parameter[0] == 63 and not intermediate:
                params = _parse_params(parameter[1:])
                if final == 104:
                    modes = self._set_modes(params)
                    if modes:
                        context.puts('\x1b[?%sh' % (';').join(modes))
                    return True
                elif final == 108:
                    modes = self._reset_modes(params)
                    if modes:
                        context.puts('\x1b[?%sl' % (';').join(modes))
                    return True
        return False

    def _set_modes(self, params):
        modes = []
        for param in params:
            if param >= 100:
                if param == MOUSE_PROTOCOL_NORMAL:
                    self.setprotocol(MOUSE_PROTOCOL_NORMAL)
                    modes.append(str(param))
                elif param == MOUSE_PROTOCOL_HIGHLIGHT:
                    self.setprotocol(MOUSE_PROTOCOL_HIGHLIGHT)
                    modes.append(str(param))
                elif param == MOUSE_PROTOCOL_BUTTON_EVENT:
                    self.setprotocol(MOUSE_PROTOCOL_BUTTON_EVENT)
                    modes.append(str(param))
                elif param == MOUSE_PROTOCOL_ANY_EVENT:
                    self.setprotocol(MOUSE_PROTOCOL_ANY_EVENT)
                    modes.append(str(param))
                elif param == FOCUS_EVENT_TRACKING:
                    self.setfocusmode(FOCUS_EVENT_TRACKING)
                elif param == MOUSE_ENCODING_UTF8:
                    self.setencoding(MOUSE_ENCODING_UTF8)
                elif param == MOUSE_ENCODING_URXVT:
                    self.setencoding(MOUSE_ENCODING_URXVT)
                elif param == MOUSE_ENCODING_SGR:
                    self.setencoding(MOUSE_ENCODING_SGR)
                elif param == 8840:
                    self._termprop.set_cjk()
                    modes.append(str(param))
                elif param == 8428:
                    self._termprop.set_noncjk()
                    modes.append(str(param))
                elif param == 8441:
                    self._listener.notifyimeon()
                elif param >= 8860:
                    if param < 8870:
                        self._listener.notifyenabled(param) or modes.append(str(param))
                else:
                    modes.append(str(param))
            else:
                modes.append(str(param))

        return modes

    def _reset_modes(self, params):
        modes = []
        for param in params:
            if param >= 1000:
                if param == MOUSE_PROTOCOL_NORMAL:
                    self.setprotocol(0)
                    modes.append(str(param))
                elif param == MOUSE_PROTOCOL_HIGHLIGHT:
                    self.setprotocol(0)
                    modes.append(str(param))
                elif param == MOUSE_PROTOCOL_BUTTON_EVENT:
                    self.setprotocol(0)
                    modes.append(str(param))
                elif param == MOUSE_PROTOCOL_ANY_EVENT:
                    self.setprotocol(0)
                    modes.append(str(param))
                elif param == FOCUS_EVENT_TRACKING:
                    self.setfocusmode(0)
                elif param == MOUSE_ENCODING_UTF8:
                    self.setencoding(0)
                elif param == MOUSE_ENCODING_URXVT:
                    self.setencoding(0)
                elif param == MOUSE_ENCODING_SGR:
                    self.setencoding(0)
                elif param == 8840:
                    self._termprop.set_noncjk()
                    modes.append(str(param))
                elif param == 8428:
                    self._termprop.set_cjk()
                    modes.append(str(param))
                elif param == 8441:
                    self._listener.notifyimeoff()
                elif param >= 8860:
                    if param < 8870:
                        self._listener.notifydisabled(param) or modes.append(str(param))
                else:
                    modes.append(str(param))
            else:
                modes.append(str(param))

        return modes


class MouseDecoder(tff.DefaultHandler):
    always_handle = True

    def __init__(self, listener, termprop, mousemode):
        self._mouse_state = None
        self._x = -1
        self._y = -1
        self._lastclick = 0
        self._mousedown = False
        self._mousedrag = False
        self._init_glich_time = None
        self.mouse_mode = mousemode
        self._termprop = termprop
        self._listener = listener
        return

    def handle_csi(self, context, parameter, intermediate, final):
        """ """
        if self.mouse_mode:
            try:
                mouse_info = self._decode_mouse(context, parameter, intermediate, final)
                if mouse_info:
                    if self._init_glich_time:
                        if time.time() - self._init_glich_time < 0.5:
                            self._init_glich_time = None
                            return False
                        self._init_glich_time = None
                    (mode, mouseup, code, x, y) = mouse_info
                    if mode == MOUSE_PROTOCOL_NORMAL:
                        self._mouse_state = []
                        return True
                    elif self.always_handle or self._listener.mouseenabled():
                        if mouseup:
                            code |= 3
                        self._dispatch_mouse(context, code, x, y)
                        return True
                    if self.mouse_mode.getprotocol() == MOUSE_ENCODING_SGR:
                        if mode == MOUSE_ENCODING_SGR:
                            return False
                        elif mode == MOUSE_ENCODING_URXVT:
                            params = (
                             code + 32, x, y)
                            context.puts('\x1b[%d;%d;%dM' % params)
                            return True
                        elif mode == MOUSE_PROTOCOL_NORMAL:
                            params = (
                             min(126, code) + 32, x + 32, y + 32)
                            context.puts('\x1b[M%c%c%c' % params)
                            return True
                        return True
                    if self.mouse_mode.getprotocol() == MOUSE_ENCODING_URXVT:
                        if mode == MOUSE_ENCODING_URXVT:
                            return False
                        elif mode == MOUSE_ENCODING_SGR:
                            params = (
                             code + 32, x, y)
                            if mouseup:
                                context.puts('\x1b[%d;%d;%dm' % params)
                            else:
                                context.puts('\x1b[%d;%d;%dM' % params)
                            return True
                        elif mode == MOUSE_PROTOCOL_NORMAL:
                            params = (
                             min(126, code) + 32, x + 32, y + 32)
                            context.puts('\x1b[M%c%c%c' % params)
                            return True
                    else:
                        return True
            finally:
                pass

        if not intermediate:
            if not parameter:
                if final == 73:
                    self._listener.onfocusin()
                    return True
                elif final == 79:
                    self._listener.onfocusout()
                    return True
        return False

    def initialize_mouse(self, output):
        self.mouse_mode.setenabled(output, True)
        self._x = -1
        self._y = -1
        self._init_glich_flag = time.time()

    def uninitialize_mouse(self, output):
        self.mouse_mode.setenabled(output, False)
        self._init_glich_flag = None
        return

    def handle_char(self, context, c):
        if self._mouse_state is not None:
            if c >= 32 and c < 127:
                self._mouse_state.append(c - 32)
                if len(self._mouse_state) == 3:
                    (code, x, y) = self._mouse_state
                    self._mouse_state = None
                    if self.always_handle or self._listener.mouseenabled():
                        self._dispatch_mouse(context, code, x - 1, y - 1)
                    if self.mouse_mode.getprotocol() != 0:
                        params = (
                         code + 32, x + 32, y + 32)
                        context.puts('\x1b[M%c%c%c' % params)
                return True
        return False

    def _decode_mouse(self, context, parameter, intermediate, final):
        if not parameter:
            if final == 77:
                return (
                 MOUSE_PROTOCOL_NORMAL, None, None, None, None)
            return
        elif parameter[0] == 60:
            if final == 77:
                p = ('').join([ chr(c) for c in parameter[1:] ])
                try:
                    params = [ int(c) for c in p.split(';') ]
                    if len(params) != 3:
                        return False
                    (code, x, y) = params
                    x -= 1
                    y -= 1
                except ValueError:
                    return False
                else:
                    return (
                     MOUSE_ENCODING_SGR, False, code, x, y)
            elif final == 109:
                p = ('').join([ chr(c) for c in parameter[1:] ])
                try:
                    params = [ int(c) for c in p.split(';') ]
                    if len(params) != 3:
                        return False
                    (code, x, y) = params
                    x -= 1
                    y -= 1
                except ValueError:
                    return
                else:
                    return (
                     MOUSE_ENCODING_SGR, True, code, x, y)
        elif 48 <= parameter[0] and parameter[0] <= 57:
            if final == 77:
                p = ('').join([ chr(c) for c in parameter ])
                try:
                    params = [ int(c) for c in p.split(';') ]
                    if len(params) != 3:
                        return False
                    (code, x, y) = params
                    code -= 32
                    x -= 1
                    y -= 1
                except ValueError:
                    return False
                else:
                    return (
                     1015, False, code, x, y)
        return

    def _dispatch_mouse(self, context, code, x, y):
        if code & 32:
            if x != self._x or y != self._y:
                if self._mousedrag:
                    self._listener.ondragmove(context, x, y)
                elif self._mousedown:
                    self._mousedrag = True
                    self._listener.ondragstart(context, x, y)
                else:
                    self._listener.onmousehover(context, x, y)
            self._x = x
            self._y = y
        elif code & 3 == 3:
            if self._mousedown:
                self._mousedown = False
                if self._mousedrag:
                    self._mousedrag = False
                    self._listener.ondragend(context, x, y)
                elif x == self._x and y == self._y:
                    now = time.time()
                    if now - self._lastclick < _DOUBLE_CLICK_SPAN:
                        self._listener.ondoubleclick(context, x, y)
                    else:
                        self._listener.onclick(context, x, y)
                    self._lastclick = now
                self._listener.onmouseup(context, x, y)
            else:
                if x != self._x or y != self._y:
                    self._listener.onmousehover(context, x, y)
                self._x = x
                self._y = y
        elif code & 64:
            if code & 1:
                self._listener.onscrollup(context, x, y)
            else:
                self._listener.onscrolldown(context, x, y)
        else:
            self._x = x
            self._y = y
            self._listener.onmousedown(context, x, y)
            self._mousedown = True
            self._mousedrag = False


def test():
    import doctest
    doctest.testmod()


if __name__ == '__main__':
    test()