# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sbo/lib/python3.4/site-packages/vaitk/gui/VWidget.py
# Compiled at: 2015-05-02 14:14:14
# Size of source mod 2**32: 21184 bytes
from .. import core
from ..consts import Index
from .. import FocusPolicy
from .VApplication import VApplication
from .VPalette import VPalette
from .VPainter import VPainter
from .VScreen import VScreenArea
from . import events

class VWidget(core.VObject):

    def __init__(self, parent=None):
        if parent is None:
            parent = VApplication.vApp.rootWidget()
        super().__init__(parent)
        if self.parent() is None:
            self._geometry = (0, 0) + VApplication.vApp.screen().size()
        else:
            self._geometry = self.parent().contentsRect()
        self._layout = None
        self._visible_implicit = False
        self._visible_explicit = None
        self._palette = None
        self._enabled = True
        self._active = True
        self._focus_policy = FocusPolicy.NoFocus
        self._needs_update = False
        self._minimum_size = (0, 0)
        self._is_window = False

    def setFocus(self, reason=None):
        """
        Gives focus to this widget.
        Arguments:
            reason: The reason behind the focus change
        """
        VApplication.vApp.setFocusWidget(self)

    def hasFocus(self):
        """
        Returns:
            True if the widget has focus, otherwise False
        """
        return self is VApplication.vApp.focusWidget()

    def move(self, pos):
        """
        Sets the size to the specified amount.
        Generates an immediate VMoveEvent if the widget is visible.
        If not visible, the widget will receive it as soon as made visible

        Arguments:
            size: a 2-tuple (x, y)
        """
        if not isinstance(pos, tuple) or len(pos) != 2:
            raise TypeError('Invalid pos argument')
        self.setGeometry(pos + self.size())

    def resize(self, size):
        """
        Sets the size to the specified amount.
        Generates an immediate VResizeEvent if the widget is visible.
        If not visible, the widget will receive it as soon as made visible

        Arguments:
            size: a 2-tuple (width, height)
        """
        if not isinstance(size, tuple) or len(size) != 2:
            raise TypeError('Invalid size argument')
        self.setGeometry(self.pos() + size)

    def setGeometry(self, rect):
        old_geometry = self._geometry
        min_size = self.minimumSize()
        self._geometry = (rect[Index.RECT_X],
         rect[Index.RECT_Y],
         max(min_size[Index.SIZE_WIDTH], rect[Index.RECT_WIDTH]),
         max(min_size[Index.SIZE_HEIGHT], rect[Index.RECT_HEIGHT]))
        if self.isVisible():
            deliver_routine = VApplication.vApp.sendEvent
        else:
            deliver_routine = VApplication.vApp.postEvent
        if (old_geometry[Index.RECT_X], old_geometry[Index.RECT_Y]) != (
         self._geometry[Index.RECT_X], self._geometry[Index.RECT_Y]):
            deliver_routine(self, events.VMoveEvent())
        if (old_geometry[Index.RECT_WIDTH], old_geometry[Index.RECT_WIDTH]) != (
         self._geometry[Index.RECT_HEIGHT], self._geometry[Index.RECT_HEIGHT]):
            deliver_routine(self, events.VResizeEvent())

    def show(self):
        """
        Makes the widget visible. Equivalent to self.setVisible(True)
        """
        self.setVisible(True)

    def hide(self):
        """
        Makes the widget hidden. Equivalent to self.setVisible(False)
        """
        self.setVisible(False)

    def lower(self):
        pass

    def raise_(self):
        pass

    def close(self):
        pass

    def setVisible(self, visible):
        """
        Changes the visibility of the widget. If setVisible(True) is called on a visible widget, nothing
        happens. The same for the hidden case.
        A ShowEvent (HideEvent) is sent before (resp. after) the visibility change is performed on screen.

        Arguments:
            visible: True to set the widget to visible. False to hide it.

        """
        self.logger.info('Setting explicit visibility for %s : %s' % (str(self), str(visible)))
        visible_before = self.isVisible()
        self._visible_explicit = visible
        if visible and not visible_before:
            VApplication.vApp.postEvent(self, events.VShowEvent())
        elif not visible:
            if visible_before:
                VApplication.vApp.postEvent(self, events.VHideEvent())
        for w in self.children():
            w.setVisibleImplicit(visible)

    def setVisibleImplicit(self, visible):
        self.logger.info('Setting implicit visibility for %s : %s' % (str(self), str(visible)))
        self._visible_implicit = visible
        if visible:
            VApplication.vApp.postEvent(self, events.VShowEvent())
        else:
            VApplication.vApp.postEvent(self, events.VHideEvent())
        for w in self.children():
            w.setVisibleImplicit(visible)

    def size(self):
        """
        Returns:
            the widget current size as a 2-tuple (width, height)
        """
        return (
         self.geometry()[Index.RECT_WIDTH], self.geometry()[Index.RECT_HEIGHT])

    def rect(self):
        """
        Returns:
            The widget current rect as a 4-tuple (0, 0, width, height).
        """
        return (0, 0) + self.size()

    def absoluteRect(self):
        return self.mapToGlobal((0, 0)) + self.size()

    def geometry(self):
        """
        Returns the geometry of the widget.

        Returns:
            A 4-tuple with (x, y, width, height)
        """
        return self._geometry

    def width(self):
        """
        Returns the width of the widget.

        Returns:
            integer
        """
        return self.geometry()[Index.RECT_WIDTH]

    def height(self):
        """
        Returns the height of the widget.

        Returns:
            integer
        """
        return self.geometry()[Index.RECT_HEIGHT]

    def pos(self):
        """
        Returns the position of the widget within its parent.

        Returns:
            A 2-tuple of integers
        """
        geometry = self.geometry()
        return (geometry[Index.RECT_X], geometry[Index.RECT_Y])

    def x(self):
        """
        Returns the x position of the widget within its parent.

        Returns:
            integer
        """
        geometry = self.geometry()
        return geometry[Index.RECT_X]

    def y(self):
        """
        Returns the y position of the widget within its parent.

        Returns:
            integer
        """
        geometry = self.geometry()
        return geometry[Index.RECT_Y]

    def isVisible(self):
        """
        Returns:
            True if the widget is visible. False if hidden.
            Note that a widget is considered visible even if fully covered by an overlapping widget.
        """
        if self._visible_explicit is not None:
            return self._visible_explicit
        return self._visible_implicit

    def isVisibleTo(self, ancestor):
        pass

    def minimumSize(self):
        """
        Returns:
            a 2-tuple (width, height) with the minimum allowed size of the widget
        """
        return self._minimum_size

    def addLayout(self, layout):
        self._layout = layout
        self._layout.setParent(self)

    def mapToGlobal(self, pos):
        """
        Given a position pos in coordinates relative to this widget, return the coordinate
        in absolute screen coordinates.

        Arguments:
            pos: 2-tuple (x,y)

        Returns:
            a 2-tuple (x,y) with the absolute coordinates
        """
        top_left = self.pos()
        if self.parent() is None:
            return (pos[Index.X] + top_left[Index.X], pos[Index.Y] + top_left[Index.Y])
        parent_corner = self.parent().mapToGlobal((0, 0))
        return (parent_corner[Index.X] + top_left[Index.X] + pos[Index.X],
         parent_corner[Index.Y] + top_left[Index.Y] + pos[Index.Y])

    def screenArea(self):
        abs_pos_topleft = self.mapToGlobal((0, 0))
        return VScreenArea(VApplication.vApp.screen(), abs_pos_topleft + self.size())

    def event(self, event):
        """
        Generic event method. Gets called for all events, and dispatches to a
        more specific event handler.

        Arguments:
            event: the event.
        """
        self.logger.info('Event %s. Receiver %s' % (str(event), str(self)))
        if isinstance(event, events.VPaintEvent):
            if not self.isVisible():
                return True
            self.paintEvent(event)
            self._needs_update = False
        else:
            if isinstance(event, events.VFocusEvent):
                if self.isVisible():
                    if event.eventType() == core.VEvent.EventType.FocusIn:
                        self.focusInEvent(event)
                elif event.eventType() == core.VEvent.EventType.FocusOut:
                    self.focusOutEvent(event)
                self.update()
            else:
                if isinstance(event, events.VHideEvent):
                    self.hideEvent(event)
                    for w in self.depthFirstFullTree():
                        self.logger.info('Widget %s in tree' % str(w))
                        if not w.isVisible():
                            continue
                        self.logger.info('Repainting widget %s' % str(w))
                        w.update()

                else:
                    if isinstance(event, events.VShowEvent):
                        self.showEvent(event)
                        for w in self.depthFirstFullTree():
                            self.logger.info('Widget %s in tree' % str(w))
                            if not w.isVisible():
                                continue
                            w.update()

                    else:
                        if isinstance(event, events.VMoveEvent):
                            if not self.isVisible():
                                return True
                            self.moveEvent(event)
                            for w in self.depthFirstFullTree():
                                self.logger.info('Widget %s in tree' % str(w))
                                if not w.isVisible():
                                    continue
                                w.update()

                        else:
                            if isinstance(event, events.VResizeEvent):
                                if not self.isVisible():
                                    return True
                                self.resizeEvent(event)
                                for w in self.depthFirstFullTree():
                                    self.logger.info('Widget %s in tree' % str(w))
                                    if not w.isVisible():
                                        continue
                                    w.update()

                            else:
                                return super().event(event)
        return True

    def keyEvent(self, event):
        """
        Handle VKeyEvents.
        """
        pass

    def paintEvent(self, event):
        painter = VPainter(self)
        size = self.size()
        string = ' ' * size[Index.SIZE_WIDTH]
        for i in range(0, size[Index.SIZE_HEIGHT]):
            painter.drawText((0, i), string)

    def focusInEvent(self, event):
        self.logger.info('FocusIn event')

    def focusOutEvent(self, event):
        self.logger.info('FocusOut event')

    def hideEvent(self, event):
        self.logger.info('Hide event')

    def moveEvent(self, event):
        self.logger.info('Move event')

    def showEvent(self, event):
        self.logger.info('Show event')

    def resizeEvent(self, event):
        self.logger.info('Resize event')

    def setFocusPolicy(self, policy):
        self._focus_policy = policy

    def focusPolicy(self):
        return self._focus_policy

    def needsUpdate(self):
        return self._needs_update

    def isEnabled(self):
        """
        Returns:
            True if the widget is enabled. False otherwise.
        """
        return self._enabled

    def isEnabledTo(self, ancestor):
        pass

    def isActive(self):
        return self._active

    def setActive(self, active):
        self._active = active

    def setEnabled(self, enabled):
        """
        Enables or disables a widget.

        Arguments:
            enabled: True to enable the widget. False to disable.
        """
        self._enabled = enabled

    def palette(self):
        """
        Returns:
            the widget palette. If no palette has been set, a copy of the
            application palette will be installed the first time this method is
            called, and then returned.
        """
        if self._palette is None:
            self._palette = VApplication.vApp.palette().copy()
        return self._palette

    def setColors(self, fg=None, bg=None):
        self.palette().setColor(VPalette.ColorGroup.Active, VPalette.ColorRole.WindowText, fg)
        self.palette().setColor(VPalette.ColorGroup.Active, VPalette.ColorRole.Window, bg)

    def colors(self, color_group=VPalette.ColorGroup.Active):
        fg = self.palette().color(color_group, VPalette.ColorRole.WindowText)
        bg = self.palette().color(color_group, VPalette.ColorRole.Window)
        return (
         fg, bg)

    def currentColors(self):
        if self.isActive():
            color_group = VPalette.ColorGroup.Active
        else:
            if isEnabled(self):
                color_group = VPalette.ColorGroup.Inactive
            else:
                color_group = VPalette.ColorGroup.Disabled
        return self.colors(color_group)

    def backgroundRole(self):
        pass

    def foregroundRole(self):
        pass

    def setForegroundRole(self, role):
        pass

    def setBackgroundRole(self, role):
        pass

    def update(self):
        self._needs_update = True

    def contentsRect(self):
        margins = self.contentsMargins()
        return (margins[Index.MARGIN_LEFT],
         margins[Index.MARGIN_TOP],
         self.width() - margins[Index.MARGIN_LEFT] - margins[Index.MARGIN_RIGHT],
         self.height() - margins[Index.MARGIN_TOP] - margins[Index.MARGIN_BOTTOM])

    def contentsMargins(self):
        return (0, 0, 0, 0)

    def childrenRect(self):
        pass

    def frameGeometry(self):
        pass

    def normalGeometry(self):
        pass

    def baseSize(self):
        pass

    def frameSize(self):
        pass

    def maximumSize(self):
        pass

    def maximumWidth(self):
        pass

    def maximumHeight(self):
        pass

    def minimumHeight(self):
        pass

    def minimumWidth(self):
        pass

    def minimumSizeHint(self):
        pass

    def sizeHint(self):
        pass

    def heightForWidth(self):
        pass

    def setBaseSize(self, size):
        pass

    def setContentsMargins(self, margins):
        pass

    def setMaximumHeight(self, maxh):
        pass

    def setMaximumSize(self, max_size):
        pass

    def setMaximumWidth(self, maxw):
        pass

    def setMinimumHeight(self, minh):
        self._minimum_size = (
         self._minimum_size[Index.SIZE_WIDTH], minh)

    def setMinimumWidth(self, minw):
        self._minimum_size = (
         minw, self._minimum_size[Index.SIZE_HEIGHT])

    def setMinimumSize(self, min_size):
        self._minimum_size = min_size

    def setFixedHeight(self, height):
        pass

    def setFixedWidth(self, width):
        pass

    def setFixedSize(self, size):
        pass

    def fontInfo(self):
        pass