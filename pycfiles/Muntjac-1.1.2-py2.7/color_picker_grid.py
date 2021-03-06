# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/addon/colorpicker/color_picker_grid.py
# Compiled at: 2013-04-04 15:36:36
from muntjac.addon.colorpicker.color import Color
from muntjac.ui.abstract_component import AbstractComponent
from muntjac.addon.colorpicker.color_change_event import ColorChangeEvent
from muntjac.addon.colorpicker.color_picker import IColorChangeListener
from muntjac.addon.colorpicker.color_selector import IColorSelector
_COLOR_CHANGE_METHOD = getattr(IColorChangeListener, 'colorChanged')

class ColorPickerGrid(AbstractComponent, IColorSelector):
    """The Class ColorPickerGrid.

    @author: John Ahlroos
    @author: Richard Lincoln
    """
    CLIENT_WIDGET = None
    TYPE_MAPPING = 'com.vaadin.addon.colorpicker.ColorPickerGrid'

    def __init__(self, colors_or_rows=None, cols=None):
        """Instantiates a new color picker grid.

        @param colors_or_rows:
                   the colors or the rows
        @param columns
                   the columns
        """
        super(ColorPickerGrid, self).__init__()
        self._x = 0
        self._y = 0
        self._rows = 1
        self._columns = 1
        self._colorGrid = [
         [
          None]]
        self._changedColors = dict()
        if colors_or_rows is None:
            self._colorGrid[0][0] = Color.WHITE
        elif cols is None:
            colors = colors_or_rows
            self._rows = len(colors)
            self._columns = len(colors[0])
            self._colorGrid = colors
            for row in range(self._rows):
                for col in range(self._columns):
                    self._changedColors[(row, col)] = self._colorGrid[row][col]

            self.requestRepaint()
        else:
            rows, columns = colors_or_rows, cols
            self.removeStyleName('v-customcomponent')
            self._rows = rows
            self._columns = columns
            self._colorGrid = [ [None] * rows for _ in range(columns) ]
            self._colorGrid[0][0] = Color.WHITE
        return

    def setColorGrid(self, colors):
        """Sets the color grid.

        @param colors
                   the new color grid
        """
        self._rows = len(colors)
        self._columns = len(colors[0])
        self._colorGrid = colors
        for row in range(self._rows):
            for col in range(self._columns):
                self._changedColors[(row, col)] = self._colorGrid[row][col]

        self.requestRepaint()

    def addListener(self, listener, iface=None):
        """Adds a color change listener

        @param listener:
                   The color change listener
        """
        if isinstance(listener, IColorChangeListener) and (iface is None or issubclass(iface, IColorChangeListener)):
            self.registerListener(ColorChangeEvent, listener, _COLOR_CHANGE_METHOD)
        super(ColorPickerGrid, self).addListener(listener, iface)
        return

    def addCallback(self, callback, eventType=None, *args):
        if eventType is None:
            eventType = callback._eventType
        if issubclass(eventType, ColorChangeEvent):
            self.registerCallback(ColorChangeEvent, callback, None, *args)
        else:
            super(ColorPickerGrid, self).addCallback(callback, eventType, *args)
        return

    def removeListener(self, listener, iface=None):
        """Removes a color change listener

        @param listener:
                   The listener
        """
        if isinstance(listener, IColorChangeListener) and (iface is None or issubclass(iface, IColorChangeListener)):
            self.withdrawListener(ColorChangeEvent, listener)
        super(ColorPickerGrid, self).removeListener(listener, iface)
        return

    def removeCallback(self, callback, eventType=None):
        if eventType is None:
            eventType = callback._eventType
        if issubclass(eventType, ColorChangeEvent):
            self.withdrawCallback(ColorChangeEvent, callback)
        else:
            super(ColorPickerGrid, self).removeCallback(callback, eventType)
        return

    def getColor(self):
        return self._colorGrid[self._x][self._y]

    def setColor(self, color):
        self._colorGrid[self._x][self._y] = color
        self._changedColors[(self._x, self._y)] = color
        self.requestRepaint()

    def setPosition(self, x, y):
        """Sets the position.

        @param x:
                   the x-coordinate
        @param y:
                   the y-coordinate
        """
        if x >= 0 and x < self._columns and y >= 0 and y < self._rows:
            self._x = x
            self._y = y

    def getPosition(self):
        """Gets the position.

        @return: the position
        """
        return (
         self._x, self._y)

    def paintContent(self, target):
        target.addAttribute('rows', self._rows)
        target.addAttribute('columns', self._columns)
        if len(self._changedColors) > 0:
            colors = [
             None] * len(self._changedColors)
            XCoords = [None] * len(self._changedColors)
            YCoords = [None] * len(self._changedColors)
            counter = 0
            for p, c in self._changedColors.iteritems():
                if c is None:
                    continue
                red = '%.2x' % c.getRed()
                green = '%.2x' % c.getGreen()
                blue = '%.2x' % c.getBlue()
                color = '#' + red + green + blue
                colors[counter] = color
                XCoords[counter] = str(p[0])
                YCoords[counter] = str(p[1])
                counter += 1

            target.addVariable(self, 'changedColors', colors)
            target.addVariable(self, 'changedX', XCoords)
            target.addVariable(self, 'changedY', YCoords)
            self._changedColors.clear()
        return

    def changeVariables(self, source, variables):
        if 'selectedX' in variables and 'selectedY' in variables:
            self._x = int(str(variables['selectedX']))
            self._y = int(str(variables['selectedY']))
            self.fireColorChanged(self._colorGrid[self._y][self._x])
        if 'refresh' in variables and variables['refresh'] == False:
            for row in range(self._rows):
                for col in range(self._cols):
                    self._changedColors[(row, col)] = self._colorGrid[row][col]

            self.requestRepaint()

    def fireColorChanged(self, color):
        """Notifies the listeners that a color change has occurred

        @param color:
                   The color which it changed to
        """
        self.fireEvent(ColorChangeEvent(self, color))