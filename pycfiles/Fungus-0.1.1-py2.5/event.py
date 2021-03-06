# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyglet/window/event.py
# Compiled at: 2009-02-07 06:48:50
"""Events for `pyglet.window`.

See `Window` for a description of the window event types.
"""
__docformat__ = 'restructuredtext'
__version__ = '$Id: event.py 1669 2008-01-27 01:31:58Z Alex.Holkner $'
import sys
from pyglet.window import key
from pyglet.window import mouse

class WindowExitHandler(object):
    """Determine if the window should be closed.

    This event handler watches for the ESC key or the window close event
    and sets `self.has_exit` to True when either is pressed.  An instance
    of this class is automatically attached to all new `pyglet.window.Window`
    objects.

    :deprecated: This class's functionality is provided directly on `Window`
        in pyglet 1.1.

    :Ivariables:
        `has_exit` : bool
            True if the user wants to close the window.

    """
    has_exit = False

    def on_close(self):
        self.has_exit = True

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            self.has_exit = True


class WindowEventLogger(object):
    """Print all events to a file.

    When this event handler is added to a window it prints out all events
    and their parameters; useful for debugging or discovering which events
    you need to handle.

    Example::

        win = window.Window()
        win.push_handlers(WindowEventLogger())

    """

    def __init__(self, logfile=None):
        """Create a `WindowEventLogger` which writes to `logfile`.

        :Parameters:
            `logfile` : file-like object
                The file to write to.  If unspecified, stdout will be used.

        """
        if logfile is None:
            import sys
            logfile = sys.stdout
        self.file = logfile
        return

    def on_key_press(self, symbol, modifiers):
        print >> self.file, 'on_key_press(symbol=%s, modifiers=%s)' % (
         key.symbol_string(symbol), key.modifiers_string(modifiers))

    def on_key_release(self, symbol, modifiers):
        print >> self.file, 'on_key_release(symbol=%s, modifiers=%s)' % (
         key.symbol_string(symbol), key.modifiers_string(modifiers))

    def on_text(self, text):
        print >> self.file, 'on_text(text=%r)' % text

    def on_text_motion(self, motion):
        print >> self.file, 'on_text_motion(motion=%s)' % key.motion_string(motion)

    def on_text_motion_select(self, motion):
        print >> self.file, 'on_text_motion_select(motion=%s)' % key.motion_string(motion)

    def on_mouse_motion(self, x, y, dx, dy):
        print >> self.file, 'on_mouse_motion(x=%d, y=%d, dx=%d, dy=%d)' % (
         x, y, dx, dy)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        print >> self.file, 'on_mouse_drag(x=%d, y=%d, dx=%d, dy=%d, buttons=%s, modifiers=%s)' % (
         x, y, dx, dy,
         mouse.buttons_string(buttons), key.modifiers_string(modifiers))

    def on_mouse_press(self, x, y, button, modifiers):
        print >> self.file, 'on_mouse_press(x=%d, y=%d, button=%r, modifiers=%s)' % (
         x, y,
         mouse.buttons_string(button), key.modifiers_string(modifiers))

    def on_mouse_release(self, x, y, button, modifiers):
        print >> self.file, 'on_mouse_release(x=%d, y=%d, button=%r, modifiers=%s)' % (
         x, y,
         mouse.buttons_string(button), key.modifiers_string(modifiers))

    def on_mouse_scroll(self, x, y, dx, dy):
        print >> self.file, 'on_mouse_scroll(x=%f, y=%f, dx=%f, dy=%f)' % (
         x, y, dx, dy)

    def on_close(self):
        print >> self.file, 'on_close()'

    def on_mouse_enter(self, x, y):
        print >> self.file, 'on_mouse_enter(x=%d, y=%d)' % (x, y)

    def on_mouse_leave(self, x, y):
        print >> self.file, 'on_mouse_leave(x=%d, y=%d)' % (x, y)

    def on_expose(self):
        print >> self.file, 'on_expose()'

    def on_resize(self, width, height):
        print >> self.file, 'on_resize(width=%d, height=%d)' % (width, height)

    def on_move(self, x, y):
        print >> self.file, 'on_move(x=%d, y=%d)' % (x, y)

    def on_activate(self):
        print >> self.file, 'on_activate()'

    def on_deactivate(self):
        print >> self.file, 'on_deactivate()'

    def on_show(self):
        print >> self.file, 'on_show()'

    def on_hide(self):
        print >> self.file, 'on_hide()'

    def on_context_lost(self):
        print >> self.file, 'on_context_lost()'

    def on_context_state_lost(self):
        print >> self.file, 'on_context_state_lost()'