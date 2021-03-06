# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/qt/qtgui/extra_nexus/taurusnexuswidget.py
# Compiled at: 2019-08-19 15:09:29
"""
nexusWidget.py:
"""
from builtins import str
import numpy, posixpath
from functools import partial
from taurus.external.qt import Qt, compat
from PyMca5.PyMcaGui.io.hdf5 import HDF5Widget, HDF5Info, HDF5DatasetTable
from taurus.qt.qtgui.container import TaurusWidget
__all__ = [
 'TaurusNexusBrowser']

class NeXusInfoWidget(Qt.QTabWidget):

    def __init__(self, parent=None, info=None):
        Qt.QTabWidget.__init__(self, parent)
        self.generalInfoWidget = HDF5GeneralInfoWidget(self)
        self.attributesInfoWidget = HDF5AttributesInfoWidget(self)
        self.addTab(self.generalInfoWidget, 'General')
        self.addTab(self.attributesInfoWidget, 'Attributes')
        self.__previewWidget = None
        return

    def setInfoDict(self, info):
        self.__previewWidget = NeXusPreviewWidgetFactory(info)


class TaurusNeXusBrowser(TaurusWidget):
    """ A Browser for nexus files with optional preview. Based on PyMCA's HDF5Widget"""

    def __init__(self, *args, **kwargs):
        TaurusWidget.__init__(self, *args)
        fileModel = kwargs.get('fileModel', None)
        if fileModel is None:
            fileModel = HDF5Widget.FileModel()
        self.__fileModel = fileModel
        self.treeWidget = HDF5Widget.HDF5Widget(self.__fileModel)
        self.treeWidget.setSizePolicy(Qt.QSizePolicy(Qt.QSizePolicy.Expanding, Qt.QSizePolicy.Expanding))
        self.__previewStack = Qt.QStackedWidget()
        self.__currentPreview = None
        self.__splitter = Qt.QSplitter()
        self.__splitter.setOrientation(Qt.Qt.Vertical)
        self.__splitter.addWidget(self.treeWidget)
        self.__splitter.addWidget(self.__previewStack)
        self.setLayout(Qt.QVBoxLayout())
        self.layout().addWidget(self.__splitter)
        self.setContextMenuPolicy(Qt.Qt.ActionsContextMenu)
        self.openFileAction = Qt.QAction(Qt.QIcon.fromTheme('document-open'), 'Open Data File...', self)
        self.togglePreviewAction = Qt.QAction(Qt.QIcon('actions:view.svg'), 'Show/Hide preview', self)
        self.togglePreviewAction.setCheckable(True)
        self.togglePreviewAction.setChecked(True)
        self.addActions([self.openFileAction, self.togglePreviewAction])
        self._toolbar = Qt.QToolBar('NeXus browser toolbar')
        self._toolbar.setIconSize(Qt.QSize(16, 16))
        self._toolbar.setFloatable(False)
        self._toolbar.addActions([
         self.openFileAction, self.togglePreviewAction])
        self.layout().setMenuBar(self._toolbar)
        self.__fileModel.sigFileAppended.connect(self.treeWidget.fileAppended)
        self.treeWidget.sigHDF5WidgetSignal.connect(self.onHDF5WidgetSignal)
        self.openFileAction.triggered.connect(partial(self.openFile, fname=None))
        self.togglePreviewAction.toggled.connect(self.__previewStack.setVisible)
        self.registerConfigProperty(self.togglePreviewAction.isChecked, self.togglePreviewAction.setChecked, 'showPreview')
        return

    @Qt.pyqtSlot()
    @Qt.pyqtSlot('QString')
    def openFile(self, fname=None):
        if fname is None:
            fname, _ = compat.getOpenFileName(self, 'Choose NeXus File', '')
        if fname:
            self.__nexusFile = self.__fileModel.openFile(fname)
        return

    def onHDF5WidgetSignal(self, ddict):
        self.__previewStack.removeWidget(self.__currentPreview)
        self.__currentPreview = self.neXusPreviewWidgetFactory(ddict)
        self.__previewStack.addWidget(self.__currentPreview)
        self.__previewStack.setCurrentWidget(self.__currentPreview)

    def neXusPreviewWidgetFactory(self, ddict):
        """returns a widget showing a preview of a node in a NeXus file"""
        if ddict['type'] == 'Dataset':
            node = ddict['name']
            data = self.__nexusFile[node]
            if len(data.shape) == 1 and isinstance(data[0], (numpy.floating, numpy.integer, int, float)):
                try:
                    import pyqtgraph as pg
                    w = pg.PlotWidget()
                    w.plot(data)
                except ImportError:
                    w = HDF5DatasetTable.HDF5DatasetTable()
                    w.setDataset(data)

            else:
                w = HDF5DatasetTable.HDF5DatasetTable()
                w.setDataset(data)
        else:
            info = HDF5Info.getInfo(self.__nexusFile, ddict['name'])
            w = HDF5Info.HDF5InfoWidget()
            w.setInfoDict(info)
        return w

    def neXusWidget(self):
        return self.treeWidget

    def findNodeIndex(self, filename, nodename):
        nexus_widget = self.neXusWidget()
        file_model = nexus_widget.model()
        for node in file_model.rootItem.children:
            if node.file.filename == filename:
                file_node = node
                break
        else:
            raise Exception('Could not find file %s' % filename)

        index = file_model.index(file_node.row, 0, Qt.QModelIndex())
        node_parts = nodename.split(posixpath.sep)
        while node_parts:
            name = posixpath.basename(node_parts.pop(0))
            for child in node.children:
                child_name = posixpath.basename(child.name)
                if child_name == name:
                    node = child
                    index = file_model.index(node.row, 0, index)
                    break
            else:
                raise Exception('Could not find node %s in %s' % (
                 name, filename))

        return index

    def setCurrentNode(self, filename, nodename):
        index = self.findNodeIndex(filename, nodename)
        self.setCurrentIndex(index)

    @classmethod
    def getQtDesignerPluginInfo(cls):
        ret = TaurusWidget.getQtDesignerPluginInfo()
        ret['module'] = 'taurus.qt.qtgui.extra_nexus'
        ret['icon'] = 'designer:listview.png'
        ret['container'] = False
        ret['group'] = 'Taurus Views'
        return ret


if __name__ == '__main__':
    import sys
    from taurus.qt.qtgui.application import TaurusApplication
    if len(sys.argv) > 1:
        fname = sys.argv[1]
    else:
        fname = None
    app = TaurusApplication(sys.argv, cmd_line_parser=None)
    w = TaurusNeXusBrowser()
    w.openFile(fname)
    w.show()
    sys.exit(app.exec_())