# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pyinstruments\curvestore\tag_widget.py
# Compiled at: 2013-12-15 11:16:45
from pyinstruments.curvestore.models import CurveDB, Tag, top_level_tags
from pyinstruments.curvestore.tags import ROOT
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtCore, QtGui
from copy import deepcopy
from cPickle import dumps, load, loads
from cStringIO import StringIO

def oldest_ancestors(list_of_nodes):
    """
    returns a list where elements that are descendant of others have been removed
    """
    oldest = set()
    for node in list_of_nodes:
        ancestor = node.parent
        older_found = False
        while ancestor and not older_found:
            older_found = ancestor in list_of_nodes
            ancestor = ancestor.parent

        if not older_found:
            oldest = oldest.union([node])

    return list(oldest)


class PyMimeData(QMimeData):
    """ 
    The PyMimeData wraps a Python instance as MIME data. 
    """
    MIME_TYPE = QString('application/x-ets-qt4-instance')

    def __init__(self, data=None):
        """ 
        Initialise the instance. 
        """
        QMimeData.__init__(self)
        self._local_instance = data
        if data is not None:
            try:
                pdata = dumps(data)
            except:
                return

            self.setData(self.MIME_TYPE, dumps(data.__class__) + pdata)
        return

    @classmethod
    def coerce(cls, md):
        """ 
        Coerce a QMimeData instance to a PyMimeData instance if possible. 
        """
        if isinstance(md, cls):
            return md
        else:
            if not md.hasFormat(cls.MIME_TYPE):
                return None
            nmd = cls()
            nmd.setData(cls.MIME_TYPE, md.data())
            return nmd

    def instance(self):
        """ 
        Return the instance. 
        """
        if self._local_instance is not None:
            return self._local_instance
        else:
            io = StringIO(str(self.data(self.MIME_TYPE)))
            try:
                load(io)
                return load(io)
            except:
                pass

            return

    def instanceType(self):
        """ 
        Return the type of the instance. 
        """
        if self._local_instance is not None:
            return self._local_instance.__class__
        else:
            try:
                return loads(str(self.data(self.MIME_TYPE)))
            except:
                pass

            return


class TagModel(QAbstractItemModel):

    def __init__(self, root=ROOT, parent=None):
        super(TagModel, self).__init__(parent)
        self.treeView = parent
        self.headers = ['Tags']
        self.columns = 1
        self.root = root

    def supportedDropActions(self):
        return Qt.CopyAction | Qt.MoveAction

    def flags(self, index):
        defaultFlags = QAbstractItemModel.flags(self, index)
        if index.isValid():
            return Qt.ItemIsEditable | Qt.ItemIsDragEnabled | Qt.ItemIsDropEnabled | defaultFlags
        else:
            return Qt.ItemIsDropEnabled | defaultFlags

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.headers[section])
        return QVariant()

    def mimeTypes(self):
        types = QStringList()
        types.append('application/x-ets-qt4-instance')
        return types

    def mimeData(self, index):
        node = [ self.nodeFromIndex(i) for i in index ]
        mimeData = PyMimeData(node)
        return mimeData

    def dropMimeData(self, mimedata, action, row, column, parentIndex):
        if action == Qt.IgnoreAction:
            return True
        dragNodes = mimedata.instance()
        dragNodes = oldest_ancestors(dragNodes)
        parentNode = self.nodeFromIndex(parentIndex)
        where = parentNode.name
        if where == '':
            where = 'root'
        if not QtGui.QMessageBox.question(QtGui.QWidget(), 'Confirm move', 'Do you want to move:\n' + (',').join([ dn.name for dn in dragNodes ]) + '\nbelow: ' + where + '?!', 'Cancel', 'OK'):
            return
        for dragNode in dragNodes:
            old_index = self.index_from_fullname(dragNode.fullname)
            try:
                dragNode.move(parentNode)
            except ValueError:
                QtGui.QMessageBox.question(QtGui.QWidget(), "Can't move", 'A tag with name ' + dragNode.name + 'already exists there', 'Cancel')
            else:
                self.beginRemoveRows(old_index.parent(), old_index.row(), row + 1)
                node = self.nodeFromIndex(parentIndex)
                self.endRemoveRows()
                self.insertRow(len(parentNode) - 1, parentIndex)

        self.emit(SIGNAL('dataChanged(QModelIndex,QModelIndex)'), parentIndex, parentIndex)
        return True

    def insertRow(self, row, parent):
        return self.insertRows(row, 1, parent)

    def insertRows(self, row, count, parent):
        self.beginInsertRows(parent, row, row + (count - 1))
        self.endInsertRows()
        return True

    def remove_row(self, row, parentIndex):
        return self.remove_rows(row, 1, parentIndex)

    def remove_rows(self, row, count, parentIndex):
        self.beginRemoveRows(parentIndex, row, row + count - 1)
        node = self.nodeFromIndex(parentIndex)
        for r in range(row, row + count):
            node.removeChild(row)

        self.endRemoveRows()
        return True

    def index(self, row, column, parent):
        node = self.nodeFromIndex(parent)
        return self.createIndex(row, column, node.childAtRow(row))

    def data(self, index, role):
        if role == Qt.DecorationRole:
            return QVariant()
        if role == Qt.TextAlignmentRole:
            return QVariant(int(Qt.AlignTop | Qt.AlignLeft))
        if role == Qt.EditRole:
            node = self.nodeFromIndex(index)
            return QString(node.name)
        if role != Qt.DisplayRole:
            return QVariant()
        node = self.nodeFromIndex(index)
        if index.column() == 0:
            return QVariant(node.name + '(' + str(CurveDB.objects.filter_tag(node.fullname).count()) + ')')

    def columnCount(self, parent):
        return self.columns

    def rowCount(self, parent):
        node = self.nodeFromIndex(parent)
        if node is None:
            return 0
        else:
            return len(node)

    def parent(self, child):
        if not child.isValid():
            return QModelIndex()
        else:
            node = self.nodeFromIndex(child)
            if node is None:
                return QModelIndex()
            parent = node.parent
            if parent is None:
                return QModelIndex()
            grandparent = parent.parent
            if grandparent is None:
                return QModelIndex()
            row = grandparent.rowOfChild(parent)
            assert row != -1
            return self.createIndex(row, 0, parent)

    def nodeFromIndex(self, index):
        if index.isValid():
            return index.internalPointer()
        return self.root

    def refresh(self):
        self.beginRemoveRows(QtCore.QModelIndex(), 0, self.rowCount(QtCore.QModelIndex()))
        self.root.build_children_from_model()
        self.endRemoveRows()

    def child_from_name(self, index, name):
        for count in range(self.rowCount(index)):
            idx = self.index(count, 0, index)
            node = self.nodeFromIndex(idx)
            if node.name == name:
                return idx

    def index_from_fullname(self, fullname):
        tag_elements = fullname.split('/')
        idx = QtCore.QModelIndex()
        for name in tag_elements:
            idx = self.child_from_name(idx, name)

        return idx


class TagTreeView(QTreeView):
    value_changed = QtCore.pyqtSignal()
    refresh_requested = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(TagTreeView, self).__init__(parent)
        self.setMinimumWidth(170)
        self.myModel = TAG_MODEL
        self.setModel(self.myModel)
        self.dragEnabled()
        self.acceptDrops()
        self.showDropIndicator()
        self.setDragDropMode(QAbstractItemView.InternalMove)
        self.setSelectionMode(self.ExtendedSelection)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self._contextMenu)
        self.refresh_requested.connect(self.refresh)
        self.connect(self.model(), SIGNAL('dataChanged(QModelIndex,QModelIndex)'), self.change)
        self.refresh_requested.emit()
        self.expandAll()

    def get_tags(self):
        return self.get_selected_tags()

    def set_tags(self, tags):
        return self._set_tags(tags)

    def _set_tags(self, tags):
        self.clearSelection()
        for tag in tags:
            self.select(tag)

    def get_selected_tags(self):
        tags = [ self.model().nodeFromIndex(index).fullname for index in self.selectedIndexes()
               ]
        return tags

    def select(self, tag):
        index = self.model().index_from_fullname(tag)
        self.selectionModel().select(index, QtGui.QItemSelectionModel.Select)
        self.repaint()

    def selectionChanged(self, i1, i2):
        super(TagTreeView, self).selectionChanged(i1, i2)
        self.value_changed.emit()

    def change(self, topLeftIndex, bottomRightIndex):
        self.update(topLeftIndex)
        self.expandAll()
        self.expanded()

    def expanded(self):
        for column in range(self.model().columnCount(QModelIndex())):
            self.resizeColumnToContents(column)

    def refresh(self):
        self.model().refresh()

    def _get_tag_from_index(self, index):
        parent = self.model().nodeFromIndex(index)
        return parent.name
        parent_names = []
        while parent:
            parent_names.append(parent.name)
            parent = parent.parent

        parent_names.reverse()
        name_clicked = ''
        for string in parent_names:
            if name_clicked != '':
                name_clicked += '/'
            name_clicked += string

        return name_clicked

    def _exec_menu_at_right_place(self, menu, point):
        p = QtCore.QPoint(point)
        p.setY(p.y() + menu.height())
        where = self.mapToGlobal(p)
        menu.exec_(where)

    def _contextMenu(self, point):
        """
        Context Menu (right click on the treeWidget)
        """
        index = self.indexAt(point)
        name_clicked = self._get_tag_from_index(index)
        node_clicked = self.model().nodeFromIndex(index)

        def add_tag():
            dialog = QtGui.QInputDialog()
            dialog.setTextValue(name_clicked)
            tag, confirm = dialog.getText(QtGui.QWidget(), 'new tag', 'enter tag name', 0, '')
            tag = str(tag)
            if confirm:
                if tag.find('/') >= 0:
                    raise ValueError('tag name should not contain /')
                if tag == '':
                    raise ValueError('tag name should not be blank')
                try:
                    node_clicked.add_child(tag)
                except ValueError:
                    QtGui.QMessageBox.question(QtGui.QWidget(), "can't add", 'A tag with name ' + tag + ' already exists there', 'Cancel')
                else:
                    self.model().emit(SIGNAL('dataChanged(QModelIndex,QModelIndex)'), index, index)

        def remove_tag(dummy, name=name_clicked):
            confirm = QtGui.QMessageBox.question(QtGui.QWidget(), 'Delete ?', "Delete tag '" + name + "': are you sure ?\n" + 'Tag will be removed from all referenced curves...', 'Cancel', 'OK')
            if confirm:
                tag = node_clicked.model_tag()
                self.model().remove_row(index.row(), index.parent())
                tag.remove()

        def rename(dummy, name=name_clicked):
            dialog = QtGui.QInputDialog()
            dialog.setTextValue(name_clicked)
            proposition = name_clicked
            tag, confirm = dialog.getText(QtGui.QWidget(), 'rename tag', 'enter tag name', 0, proposition)
            if confirm:
                new_name = str(tag)
                try:
                    node_clicked.rename(new_name)
                except ValueError:
                    QtGui.QMessageBox.question(QtGui.QWidget(), "Can't rename", 'A tag with name ' + new_name + ' already exists there', 'Cancel')
                else:
                    self.model().emit(SIGNAL('dataChanged(QModelIndex,QModelIndex)'), index, index)

        menu = QtGui.QMenu(self)
        action_add_tag = QtGui.QAction('add tag...', self)
        action_add_tag.triggered.connect(add_tag)
        menu.addAction(action_add_tag)
        action_rename_tag = QtGui.QAction('rename tag', self)
        action_rename_tag.triggered.connect(rename)
        menu.addAction(action_rename_tag)
        action_remove_tag = QtGui.QAction('remove tag', self)
        action_remove_tag.triggered.connect(remove_tag)
        menu.addAction(action_remove_tag)
        action_refresh_list = QtGui.QAction('refresh list', self)
        action_refresh_list.triggered.connect(self.refresh)
        menu.addAction(action_refresh_list)
        self._exec_menu_at_right_place(menu, point)


class CurveTagWidget(QtGui.QWidget):
    value_changed = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(CurveTagWidget, self).__init__(parent)
        self.tree = TagTreeView()
        self.tree.value_changed.connect(self._update_tag_list)
        self.tag_list = QtGui.QTextEdit()
        width = self.tag_list.sizeHint().width()
        self.tag_list.setMaximumHeight(30)
        self.tag_list.setEnabled(False)
        self.lay = QtGui.QVBoxLayout()
        self.lay.addWidget(self.tree)
        self.lay.addWidget(self.tag_list)
        self.setLayout(self.lay)
        self.lay.setSpacing(0)

    def _update_tag_list(self, *args, **kwds):
        string = ''
        for tag in self.tree.get_selected_tags():
            string += "'" + tag + "' ;"

        self.tag_list.setText(string)
        self.value_changed.emit()

    def _set_tags(self, tags):
        self.tree.clearSelection()
        for tag in tags:
            self.select(tag)

    def get_tags(self):
        return self.tree.get_selected_tags()

    def set_tags(self, tags):
        return self.tree.set_tags(tags)


TAG_MODEL = TagModel(ROOT)

class DummyNode:

    def __init__(self, name):
        self.name = name


class TagStringModelOld(QtGui.QStringListModel):

    def __init__(self):
        super(TagStringModel, self).__init__()
        self.refresh_nodes()

    def refresh_nodes(self):
        self.nodes = [ DummyNode(tag.name) for tag in Tag.objects.all() ]

    def index(self, row, column, parent):
        return self.createIndex(row, column, self.nodes[row])

    def flags(self, index):
        defaultFlags = QAbstractItemModel.flags(self, index)
        if index.isValid():
            return Qt.ItemIsEditable | Qt.ItemIsDragEnabled | Qt.ItemIsDropEnabled | defaultFlags
        else:
            return Qt.ItemIsDropEnabled | defaultFlags

    def data(self, index, role):
        if role == Qt.DecorationRole:
            return QVariant()
        if role == Qt.TextAlignmentRole:
            return QVariant(int(Qt.AlignTop | Qt.AlignLeft))
        if role == Qt.EditRole:
            return QString(index.internalPointer().name)
        if role != Qt.DisplayRole:
            return QVariant()
        if index.column() == 0:
            return QVariant(index.internalPointer().name)

    def columnCount(self, parent):
        return 1

    def rowCount(self, parent):
        self.refresh_nodes()
        return len(self.nodes)