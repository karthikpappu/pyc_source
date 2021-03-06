# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/view/controls/editors/localfileeditor.py
# Compiled at: 2013-04-11 17:47:52
import os.path
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt
from customeditor import CustomEditor, set_background_color_palette
from camelot.view.art import Icon
from camelot.core.utils import ugettext as _
from camelot.view.controls.decorated_line_edit import DecoratedLineEdit

class LocalFileEditor(CustomEditor):
    """Widget for browsing local files and directories"""
    browse_icon = Icon('tango/16x16/places/folder-saved-search.png')

    def __init__(self, parent=None, field_name='local_file', directory=False, save_as=False, file_filter='All files (*)', **kwargs):
        CustomEditor.__init__(self, parent)
        self.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        self.setObjectName(field_name)
        self._directory = directory
        self._save_as = save_as
        self._file_filter = file_filter
        self.setup_widget()

    def setup_widget(self):
        """Called inside init, overwrite this method for custom
        file edit widgets"""
        layout = QtGui.QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        browse_button = QtGui.QToolButton(self)
        browse_button.setFocusPolicy(Qt.ClickFocus)
        browse_button.setIcon(self.browse_icon.getQIcon())
        browse_button.setToolTip(_('Browse'))
        browse_button.setAutoRaise(True)
        browse_button.clicked.connect(self.browse_button_clicked)
        self.filename = DecoratedLineEdit(self)
        self.filename.editingFinished.connect(self.filename_editing_finished)
        self.setFocusProxy(self.filename)
        layout.addWidget(self.filename)
        layout.addWidget(browse_button)
        self.setLayout(layout)

    @QtCore.pyqtSlot()
    def filename_editing_finished(self):
        self.valueChanged.emit()
        self.editingFinished.emit()

    @QtCore.pyqtSlot()
    def browse_button_clicked(self):
        current_directory = os.path.dirname(self.get_value())
        if self._directory:
            value = QtGui.QFileDialog.getExistingDirectory(self, directory=current_directory)
        elif self._save_as:
            value = QtGui.QFileDialog.getSaveFileName(self, filter=self._file_filter, directory=current_directory)
        else:
            value = QtGui.QFileDialog.getOpenFileName(self, filter=self._file_filter, directory=current_directory)
        value = os.path.abspath(unicode(value))
        self.filename.setText(value)
        self.valueChanged.emit()
        self.editingFinished.emit()

    def set_value(self, value):
        value = CustomEditor.set_value(self, value)
        if value:
            self.filename.setText(value)
        else:
            self.filename.setText('')
        self.valueChanged.emit()
        return value

    def get_value(self):
        return CustomEditor.get_value(self) or unicode(self.filename.text())

    value = QtCore.pyqtProperty(str, get_value, set_value)

    def set_field_attributes(self, editable=True, background_color=None, tooltip=None, **kwargs):
        self.setEnabled(editable)
        if self.filename:
            set_background_color_palette(self.filename, background_color)
            self.filename.setToolTip(unicode(tooltip or ''))