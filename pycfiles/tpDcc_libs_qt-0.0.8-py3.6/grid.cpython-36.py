# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpDcc/libs/qt/widgets/grid.py
# Compiled at: 2020-04-15 12:12:43
# Size of source mod 2**32: 3175 bytes
"""
Module that contains different grid widgets
"""
from __future__ import print_function, division, absolute_import
from Qt.QtWidgets import *
from tpDcc.libs.qt.core import base

class GridWidget(QTableWidget, object):
    __doc__ = '\n    Widget that behaves as a grid widget\n    '

    def __init__(self, parent=None):
        super(GridWidget, self).__init__(parent=parent)

    def resizeEvent(self, event):
        """
        Override resizeEvent so the table columns maintain its size when resizing QTableWidget
        :param event: QResizeEvent
        :return:
        """
        total_width = self.viewport().width()
        num_columns = self.columnCount()
        for column in range(num_columns):
            self.horizontalHeader().resizeSection(column, total_width / num_columns)

    def pos_to_row_col(self, pos):
        """
        With a given position in the grid returns the (row, column) values for that position
        :param pos: QPoint
        :return:
        """
        index = self.indexAt(pos)
        if not index:
            return
        else:
            return (
             index.row(), index.column())

    def addWidget(self, row, col, widget):
        """
        Adds a new QWidget into the given row col overriding any existing widget if already exists one
        :param row: int, row to add the widget into
        :param col: int, col to add the widget into
        :param widget: QWidget
        """
        container_widget = base.ContainerWidget(self)
        container_widget.set_contained_widget(widget)
        self.setCellWidget(row, col, container_widget)

    def add_widget_first_empty_cell(self, widget):
        """
        Adds a new QWidget into the first available cell in the grid
        :param widget: QWidget
        :return:
        """
        row, col = self.first_empty_cell()
        self.addWidget(row, col, widget)
        self.resizeRowsToContents()

    def first_empty_cell(self):
        """
        Returns the first empty cell in the table
        :return: int, int, first row, col pair of empty the first empty cell
        """
        empty_cell = (-1, -1)
        for row in range(self.rowCount()):
            for column in range(self.columnCount()):
                if not self.cellWidget(row, column):
                    empty_cell = (
                     row, column)
                    break

            if empty_cell != (-1, -1):
                break

        if empty_cell == (-1, -1):
            self.insertRow(self.rowCount())
            empty_cell = (self.rowCount() - 1, 0)
        return empty_cell

    def count(self):
        """
        Returns the total number of characters that are already loaded on the table
        :return: int, total number of characters
        """
        return self.columnCount() * self.rowCount()

    def get_widgets(self):
        for row in range(self.rowCount()):
            for column in range(self.columnCount()):
                cell_widget = self.cellWidget(row, column)
                if not cell_widget:
                    pass
                else:
                    item_widget = cell_widget.containedWidget
                    yield item_widget