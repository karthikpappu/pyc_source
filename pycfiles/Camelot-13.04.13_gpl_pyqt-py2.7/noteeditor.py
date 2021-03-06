# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/view/controls/editors/noteeditor.py
# Compiled at: 2013-04-11 17:47:52
from PyQt4 import QtGui, QtCore
from camelot.view.art import ColorScheme
from customeditor import AbstractCustomEditor

class NoteEditor(QtGui.QLabel, AbstractCustomEditor):
    """An editor that behaves like a note, the editor hides itself when
    there is no text to display"""
    editingFinished = QtCore.pyqtSignal()

    def __init__(self, parent=None, field_name='note', **kwargs):
        QtGui.QLabel.__init__(self, parent)
        AbstractCustomEditor.__init__(self)
        self.setObjectName(field_name)
        self.setTextFormat(QtCore.Qt.RichText)
        self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        style = '\n        QLabel {\n          margin: 0px;\n          padding: 3px;\n          border: 1px solid black;\n          color: black;\n          background-color: %s;\n        }\n        ' % ColorScheme.yellow_1.name()
        self.setStyleSheet(style)

    def set_value(self, value):
        value = super(NoteEditor, self).set_value(value)
        self.setVisible(value != None)
        if value:
            self.setText(unicode(value))
        return