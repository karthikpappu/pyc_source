# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/qt/qtgui/qwt5/curveprops.py
# Compiled at: 2019-08-19 15:09:30
"""
curveprops: Model and view for curve properties
"""
from __future__ import absolute_import
from builtins import str
from builtins import bytes
from builtins import object
import copy
from taurus.external.qt import Qt, Qwt5
import taurus, taurus.core
from taurus.core import TaurusElementType
from taurus.qt.qtcore.mimetypes import TAURUS_MODEL_LIST_MIME_TYPE, TAURUS_ATTR_MIME_TYPE
from taurus.qt.qtgui.util.ui import UILoadable
from .curvesAppearanceChooserDlg import NamedLineStyles, ReverseNamedLineStyles, NamedCurveStyles, ReverseNamedCurveStyles, NamedSymbolStyles, ReverseNamedSymbolStyles, NamedColors, CurveAppearanceProperties
__all__ = [
 'CurveConf', 'CurvesTableModel',
 'ExtendedSelectionModel', 'CurvePropertiesView']
NUMCOLS = 4
X, Y, TITLE, VIS = list(range(NUMCOLS))
SRC_ROLE = Qt.Qt.UserRole + 1
PROPS_ROLE = Qt.Qt.UserRole + 2
from taurus import isValidName

class Component(object):

    def __init__(self, src):
        self.src = src
        self.display = ''
        self.icon = Qt.QIcon()
        self.ok = True
        self._dbCache = taurus.Authority()
        self.setSrc(src)

    def update(self):
        self.setSrc(self.src)

    def setSrc(self, src):
        self.src, self.display, self.icon, self.ok = self.processSrc(src)

    def processSrc(self, src):
        """returns src,display,icon,ok"""
        src = str(src)
        if src == '':
            return ('', '', Qt.QIcon(), True)
        if src.startswith('='):
            return (
             src, src[1:].strip(), Qt.QIcon.fromTheme('accessories-calculator'), True)
        if isValidName(src, etypes=[TaurusElementType.Attribute]):
            return (src, src, Qt.QIcon.fromTheme('network-server'), True)
        return (src, src, Qt.QIcon.fromTheme('dialog-warning'), False)


class CurveConf(object):

    def __init__(self, xsrc='', ysrc='', properties=None, title='', vis=Qwt5.QwtPlot.yLeft):
        if properties is None:
            properties = CurveAppearanceProperties()
        self.properties = properties
        self.title = title
        self.vis = vis
        self.x = Component(xsrc)
        self.y = Component(ysrc)
        return

    def __repr__(self):
        ret = "CurveConf(xsrc='%s', ysrc='%s', title='%s')" % (
         self.x.src, self.y.src, self.title)
        return ret


class CurvesTableModel(Qt.QAbstractTableModel):
    """ A model to manage information about curves to be plotted an their appearance
    """
    dataChanged = Qt.pyqtSignal('QModelIndex', 'QModelIndex')

    def __init__(self, curves=None):
        if curves is None:
            curves = []
        super(CurvesTableModel, self).__init__()
        self.ncolumns = NUMCOLS
        self.curves = curves
        return

    def addCurve(self, curveconf):
        self.curves.append(curveconf)

    def dumpData(self):
        return copy.copy(self.curves)

    def rowCount(self, index=Qt.QModelIndex()):
        return len(self.curves)

    def columnCount(self, index=Qt.QModelIndex()):
        return self.ncolumns

    def data(self, index, role=Qt.Qt.DisplayRole):
        if not index.isValid() or not 0 <= index.row() < self.rowCount():
            return
        row = index.row()
        column = index.column()
        if role == Qt.Qt.DisplayRole:
            if column == X:
                return str(self.curves[row].x.display)
            else:
                if column == Y:
                    return str(self.curves[row].y.display)
                if column == TITLE:
                    return str(self.curves[row].title)
                if column == VIS:
                    return str(self.curves[row].vis)
                return

        elif role == Qt.Qt.DecorationRole:
            if column == X:
                return self.curves[row].x.icon
            else:
                if column == Y:
                    return self.curves[row].y.icon
                if column == TITLE:
                    return Qt.QColor(self.curves[row].properties.lColor or 'black')
                return

        elif role == Qt.Qt.TextColorRole:
            if column == X:
                Qt.QColor(self.curves[row].x.ok and 'green' or 'red')
            elif column == Y:
                Qt.QColor(self.curves[row].y.ok and 'green' or 'red')
            else:
                return
        else:
            if role == SRC_ROLE:
                if column == X:
                    return str(self.curves[row].x.src)
                else:
                    if column == Y:
                        return str(self.curves[row].y.src)
                    return

            elif role == PROPS_ROLE:
                return self.curves[row].properties
            if role == Qt.Qt.ToolTipRole:
                if column == X:
                    return str(self.curves[row].x.src)
                else:
                    if column == Y:
                        return str(self.curves[row].y.src)
                    return

        if role == Qt.Qt.EditRole:
            if column == X:
                return str(self.curves[row].x.src)
            else:
                if column == Y:
                    return str(self.curves[row].y.src)
                if column == TITLE:
                    return str(self.curves[row].title)
                return

        return

    def headerData(self, section, orientation, role=Qt.Qt.DisplayRole):
        if role == Qt.Qt.TextAlignmentRole:
            if orientation == Qt.Qt.Horizontal:
                return int(Qt.Qt.AlignLeft | Qt.Qt.AlignVCenter)
            return int(Qt.Qt.AlignRight | Qt.Qt.AlignVCenter)
        else:
            if role != Qt.Qt.DisplayRole:
                return
            else:
                if orientation == Qt.Qt.Horizontal:
                    if section == X:
                        return 'X source'
                    if section == Y:
                        return 'Y Source'
                    if section == TITLE:
                        return 'Title'
                    if section == VIS:
                        return 'Shown at'
                    return
                return str(section + 1)

            return

    def flags(self, index):
        if not index.isValid():
            return Qt.Qt.ItemIsEnabled
        column = index.column()
        if column in (X, Y):
            return Qt.Qt.ItemFlags(Qt.Qt.ItemIsEnabled | Qt.Qt.ItemIsEditable | Qt.Qt.ItemIsDragEnabled | Qt.Qt.ItemIsDropEnabled | Qt.Qt.ItemIsSelectable)
        if column == TITLE:
            return Qt.Qt.ItemFlags(Qt.Qt.ItemIsEnabled | Qt.Qt.ItemIsDragEnabled)
        return Qt.Qt.ItemFlags(Qt.Qt.ItemIsEnabled | Qt.Qt.ItemIsEditable | Qt.Qt.ItemIsDragEnabled)

    def setData(self, index, value=None, role=Qt.Qt.EditRole):
        if index.isValid() and 0 <= index.row() < self.rowCount():
            row = index.row()
            curve = self.curves[row]
            if role == PROPS_ROLE:
                self.curves[row].properties = value
                self.dataChanged.emit(self.index(row, 0), self.index(row, self.ncolumns - 1))
            else:
                column = index.column()
                if column == X:
                    curve.x.setSrc(value)
                elif column == Y:
                    curve.y.setSrc(value)
                elif column == TITLE:
                    curve.title = value
                elif column == VIS:
                    curve.vis = value
                self.dataChanged.emit(index, index)
            return True
        return False

    def insertRows(self, position=None, rows=1, parentindex=None):
        if position is None:
            position = self.rowCount()
        if parentindex is None:
            parentindex = Qt.QModelIndex()
        self.beginInsertRows(parentindex, position, position + rows - 1)
        slice = [ CurveConf() for i in range(rows) ]
        self.curves = self.curves[:position] + slice + self.curves[position:]
        self.endInsertRows()
        return True

    def removeRows(self, position, rows=1, parentindex=None):
        if parentindex is None:
            parentindex = Qt.QModelIndex()
        self.beginResetModel()
        self.beginRemoveRows(parentindex, position, position + rows - 1)
        self.curves = self.curves[:position] + self.curves[position + rows:]
        self.endRemoveRows()
        self.endResetModel()
        return True

    def mimeTypes(self):
        result = list(Qt.QAbstractTableModel.mimeTypes(self))
        result += [TAURUS_ATTR_MIME_TYPE, 'text/plain']
        return result

    def dropMimeData(self, data, action, row, column, parent):
        if row == -1:
            if parent.isValid():
                row = parent.row()
            else:
                row = parent.rowCount()
        if column == -1:
            if parent.isValid():
                column = parent.column()
            else:
                column = parent.columnCount()
        if data.hasFormat(TAURUS_ATTR_MIME_TYPE):
            model = bytes(data.data(TAURUS_ATTR_MIME_TYPE)).decode('utf-8')
            self.setData(self.index(row, column), value=model)
            return True
        if data.hasFormat(TAURUS_MODEL_LIST_MIME_TYPE):
            d = bytes(data.data(TAURUS_MODEL_LIST_MIME_TYPE))
            models = d.decode('utf-8').split()
            if len(models) == 1:
                self.setData(self.index(row, column), value=models[0])
                return True
            self.insertRows(row, len(models))
            for i, m in enumerate(models):
                self.setData(self.index(row + i, column), value=m)

            return True
        elif data.hasText():
            self.setData(self.index(row, column), data.text())
            return True
        return False

    def mimeData(self, indexes):
        mimedata = Qt.QAbstractTableModel.mimeData(self, indexes)
        if len(indexes) == 1:
            txt = self.data(indexes[0], role=SRC_ROLE)
            mimedata.setText(txt)
        return mimedata


class ExtendedSelectionModel(Qt.QItemSelectionModel):
    """A QItemSelectionModel subclass that provides :meth:`partiallySelectedRows`"""

    def partiallySelectedRows(self):
        """
        Returns the row numbers of those rows for which at least one column is selected.

        :return: (list<QModelIndex>) a list of indexes corresponding to the
                 first column of the (partially) selected curves
        """
        temp = []
        for index in self.selectedIndexes():
            row = index.row()
            if row not in temp:
                temp.append(row)

        model = self.model()
        return [ model.index(row, 0) for row in temp ]


@UILoadable(with_ui='ui')
class CurvePropertiesView(Qt.QAbstractItemView):
    """This widget is a view on a CurvesTableModel. It displays and allows to change the
    properties of selected curve(s). Note that this widget does not allow to
    change selection by itself, but rather relies on some other view on the same
    model (like a QTableView) to alter the selection.
    """

    def __init__(self, parent=None, designMode=False):
        super(CurvePropertiesView, self).__init__(parent)
        self.loadUi()
        self.ui.sStyleCB.insertItems(0, sorted(NamedSymbolStyles.values()))
        self.ui.lStyleCB.insertItems(0, list(NamedLineStyles.values()))
        self.ui.cStyleCB.insertItems(0, list(NamedCurveStyles.values()))
        self.ui.sColorCB.addItem('')
        self.ui.lColorCB.addItem('')
        for color in NamedColors:
            icon = self._colorIcon(color)
            self.ui.sColorCB.addItem(icon, '', Qt.QColor(color))
            self.ui.lColorCB.addItem(icon, '', Qt.QColor(color))

        self._emptyProps = CurveAppearanceProperties()
        self.showProperties(self._emptyProps)
        self.ui.sStyleCB.currentIndexChanged.connect(self._onSymbolStyleChanged)
        self.ui.sStyleCB.currentIndexChanged.connect(self.onPropertyControlChanged)
        self.ui.lStyleCB.currentIndexChanged.connect(self.onPropertyControlChanged)
        self.ui.lStyleCB.currentIndexChanged.connect(self.onPropertyControlChanged)
        self.ui.lColorCB.currentIndexChanged.connect(self.onPropertyControlChanged)
        self.ui.sColorCB.currentIndexChanged.connect(self.onPropertyControlChanged)
        self.ui.cStyleCB.currentIndexChanged.connect(self.onPropertyControlChanged)
        self.ui.sSizeSB.valueChanged.connect(self.onPropertyControlChanged)
        self.ui.lWidthSB.valueChanged.connect(self.onPropertyControlChanged)
        self.ui.sFillCB.stateChanged.connect(self.onPropertyControlChanged)
        self.ui.cFillCB.stateChanged.connect(self.onPropertyControlChanged)

    def dataChanged(self, topleft, bottomright):
        """Reimplemented. See :meth:`Qt.QAbstractItemView.dataChanged` """
        Qt.QAbstractItemView.dataChanged(self, topleft, bottomright)
        minrow = topleft.row()
        maxrow = bottomright.row()
        for index in self.selectionModel().partiallySelectedRows():
            row = index.row()
            if row > minrow and row < maxrow:
                self.updateControls()
                return

    def selectionChanged(self, selected, deselected):
        """Reimplemented. See :meth:`Qt.QAbstractItemView.selectionChanged` """
        Qt.QAbstractItemView.selectionChanged(self, selected, deselected)
        self.updateControls()

    def indexAt(self, *args, **kwargs):
        """ dummy reimplementation"""
        return Qt.QModelIndex()

    def visualRect(self, *args, **kwargs):
        """ dummy reimplementation"""
        return Qt.QRect()

    def verticalOffset(self, *args, **kwargs):
        """ dummy reimplementation"""
        return 0

    def horizontalOffset(self, *args, **kwargs):
        """ dummy reimplementation"""
        return 0

    def visualRegionForSelection(self, *args, **kwargs):
        """ dummy reimplementation"""
        return Qt.QRegion()

    def scrollTo(self, *args, **kwargs):
        """ dummy reimplementation"""
        pass

    def _onSymbolStyleChanged(self, text):
        """Slot called when the Symbol style is changed, to ensure that symbols
        are visible if you choose them

        :param text: (str) the new symbol style label
        """
        text = str(text)
        if self.ui.sSizeSB.value() < 2 and text not in ('', 'No symbol'):
            self.ui.sSizeSB.setValue(3)

    def blockControlsSignals(self, block):
        """blocks/unblocks the signals from all the properties controls

        :param block: (bool) If True, signals are blocked. If False they are unblocked
        """
        self.ui.sStyleCB.blockSignals(block)
        self.ui.lStyleCB.blockSignals(block)
        self.ui.lColorCB.blockSignals(block)
        self.ui.cStyleCB.blockSignals(block)
        self.ui.sSizeSB.blockSignals(block)
        self.ui.lWidthSB.blockSignals(block)
        self.ui.sFillCB.blockSignals(block)
        self.ui.cFillCB.blockSignals(block)
        self.ui.sColorCB.blockSignals(block)

    def updateControls(self):
        """Updates the state of the properties controls to reflect the selection
        """
        selectedCurves = self.selectionModel().partiallySelectedRows()
        self.showProperties(self._emptyProps)
        if len(selectedCurves) < 1:
            return
        modeldata = self.model().data
        props = [ modeldata(index, PROPS_ROLE) for index in selectedCurves ]
        mergedprop = CurveAppearanceProperties.merge(props, conflict=CurveAppearanceProperties.inConflict_none)
        self.showProperties(mergedprop)

    def onPropertyControlChanged(self, *args):
        """slot called whenever one of the controls is changed """
        shownprop = self.getShownProperties()
        data = self.model().data
        setData = self.model().setData
        for index in self.selectionModel().partiallySelectedRows():
            prop = data(index, PROPS_ROLE)
            if prop.conflictsWith(shownprop):
                updatedprop = CurveAppearanceProperties.merge([
                 prop, shownprop], conflict=CurveAppearanceProperties.inConflict_update_a)
                setData(index, updatedprop, PROPS_ROLE)

    def showProperties(self, prop, blockSignals=True):
        """Updates the control widgets to show the given properties.

         ..note:: that the signals of the controls may be temporally blocked to
                  prevent loops. See the `blockSignals` parameter.

        :param prop: (CurveAppearanceProperties) the properties object
                     containing what should be shown. If a given property is set
                     to None, the corresponding widget will show a "neutral"
                     display
        :param blockSignals: (bool) If True (default) the signals of the control widgets
                             are blocked while updating them to avoid loops.
        """
        if blockSignals:
            self.blockControlsSignals(True)
        self.ui.sStyleCB.setCurrentIndex(self.ui.sStyleCB.findText(NamedSymbolStyles[prop.sStyle]))
        self.ui.lStyleCB.setCurrentIndex(self.ui.lStyleCB.findText(NamedLineStyles[prop.lStyle]))
        self.ui.cStyleCB.setCurrentIndex(self.ui.cStyleCB.findText(NamedCurveStyles[prop.cStyle]))
        self.ui.sSizeSB.setValue(max(prop.sSize, -1))
        self.ui.lWidthSB.setValue(max(prop.lWidth, -1))
        if prop.sColor is None:
            index = 0
        else:
            index = self.ui.sColorCB.findData(Qt.QColor(prop.sColor))
        if index == -1:
            index = self.ui.sColorCB.count()
            self.ui.sColorCB.addItem(self._colorIcon(Qt.QColor(prop.sColor)), '', Qt.QColor(prop.sColor))
        self.ui.sColorCB.setCurrentIndex(index)
        if prop.lColor is None:
            index = 0
        else:
            index = self.ui.lColorCB.findData(Qt.QColor(prop.lColor))
        if index == -1:
            index = self.ui.lColorCB.count()
            self.ui.lColorCB.addItem(self._colorIcon(Qt.QColor(prop.lColor)), '', Qt.QColor(prop.lColor))
        self.ui.lColorCB.setCurrentIndex(index)
        if prop.sFill is None:
            checkState = Qt.Qt.PartiallyChecked
        elif prop.sFill:
            checkState = Qt.Qt.Checked
        else:
            checkState = Qt.Qt.Unchecked
        self.ui.sFillCB.setCheckState(checkState)
        if prop.cFill is None:
            checkState = Qt.Qt.PartiallyChecked
        elif prop.cFill:
            checkState = Qt.Qt.Checked
        else:
            checkState = Qt.Qt.Unchecked
        self.ui.cFillCB.setCheckState(checkState)
        if blockSignals:
            self.blockControlsSignals(False)
        return

    def getShownProperties(self):
        """Returns a copy of the currently shown properties

        :return: (CurveAppearanceProperties)
        """
        prop = CurveAppearanceProperties()
        prop.sStyle = ReverseNamedSymbolStyles[str(self.ui.sStyleCB.currentText())]
        prop.lStyle = ReverseNamedLineStyles[str(self.ui.lStyleCB.currentText())]
        prop.cStyle = ReverseNamedCurveStyles[str(self.ui.cStyleCB.currentText())]
        prop.sSize = self.ui.sSizeSB.value()
        prop.lWidth = self.ui.lWidthSB.value()
        if prop.sSize < 0:
            prop.sSize = None
        if prop.lWidth < 0:
            prop.lWidth = None
        index = self.ui.sColorCB.currentIndex()
        if index == 0:
            prop.sColor = None
        else:
            prop.sColor = Qt.QColor(self.ui.sColorCB.itemData(index))
        index = self.ui.lColorCB.currentIndex()
        if index == 0:
            prop.lColor = None
        else:
            prop.lColor = Qt.QColor(self.ui.lColorCB.itemData(index))
        checkState = self.ui.sFillCB.checkState()
        if checkState == Qt.Qt.PartiallyChecked:
            prop.sFill = None
        else:
            prop.sFill = bool(checkState)
        checkState = self.ui.cFillCB.checkState()
        if checkState == Qt.Qt.PartiallyChecked:
            prop.cFill = None
        else:
            prop.cFill = bool(checkState)
        return copy.deepcopy(prop)

    def _colorIcon(self, color, w=10, h=10):
        """returns an icon consisting of a rectangle of the given color

        :param color: (QColor or something accepted by QColor creator) The color for the icon
        :param w: (int) width of the icon
        :param h: (int) height of the icon

        :return: (QIcon)
        """
        pixmap = Qt.QPixmap(w, h)
        pixmap.fill(Qt.QColor(color))
        return Qt.QIcon(pixmap)


def main():
    from taurus.qt.qtgui.application import TaurusApplication
    app = TaurusApplication(sys.argv, cmd_line_parser=None)
    curves = [
     CurveConf(xsrc='', ysrc='tango://host:1000/a/b/c/d', properties=None, title='tangocurve', vis=Qwt5.QwtPlot.yLeft),
     CurveConf(xsrc='=[1,2,3]', ysrc='=#2.x**2', properties=None, title='parab', vis=Qwt5.QwtPlot.yLeft)]
    form = CurvePropertiesView()
    form.setModel(CurvesTableModel(curves))
    form.show()
    sys.exit(app.exec_())
    return


if __name__ == '__main__':
    import sys
    main()