# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.4/dist-packages/quickcut/widgets.py
# Compiled at: 2015-09-13 11:53:14
# Size of source mod 2**32: 5560 bytes
import os
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QValidator
from PyQt5.QtWidgets import QLineEdit, QPushButton, QFileDialog, QMessageBox
__author__ = 'eoubrayrie'
lastDir = os.path.expandvars('$HOME')

class FileValidator(QValidator):

    def __init__(self, *args, is_file=True, is_writable=False):
        super().__init__(*args)
        self.is_file = is_file
        self.is_writable = is_writable

    def validate(self, s, pos):
        if not s:
            return (QValidator.Intermediate, s, pos)
        news = os.path.abspath(s)
        if news != s:
            pos = pos + len(news) - len(s)
            s = news
        if self.is_file and not os.path.isfile(s):
            return (QValidator.Intermediate, s, pos)
        if self.is_writable and not ((not os.path.isfile(s) or os.access(s, os.W_OK)) and os.access(os.path.dirname(s), os.W_OK) and not os.path.isdir(s)):
            return (QValidator.Intermediate, s, pos)
        return (QValidator.Acceptable, s, pos)

    def fixup(self, s):
        pass


class Picker(QtWidgets.QWidget):

    def __init__(self, title, label='Select', check_exists=True, check_writable=False, filters=None):
        """
        :param title: tile of the actual picker window
        :param label: button text
        :param check_exists: if true, file must exist (e.g. 'Open' dialog)
        :param check_writable: if true, location must be check_writable (e.g. 'Save' dialog)
        :param filters: files to display (in Qt's own syntax)
        """
        super(Picker, self).__init__()
        self.save = check_writable
        self.title = title
        self.filters = filters
        hbox = QtWidgets.QHBoxLayout()
        self.wtext = ValidatedLineEdit(FileValidator(is_file=check_exists, is_writable=check_writable), self)
        self.wtext.setMinimumWidth(300)
        hbox.addWidget(self.wtext)
        self.textChanged = self.wtext.textChanged
        self.hasAcceptableInput = self.wtext.hasAcceptableInput
        self.set_text = self.wtext.setText
        icon = self.style().standardIcon(QtWidgets.QStyle.SP_DialogOpenButton)
        self.wbtn = QPushButton(icon, label, self)
        self.wbtn.clicked.connect(self.pick)
        hbox.addWidget(self.wbtn)
        self.setLayout(hbox)

    @pyqtSlot()
    def pick(self):
        dlg = QFileDialog(self, self.title, lastDir, self.filters)
        if self.save:
            dlg.setAcceptMode(QFileDialog.AcceptSave)
        else:
            dlg.setAcceptMode(QFileDialog.AcceptOpen)
            dlg.setFileMode(QFileDialog.ExistingFile)
        if not dlg.exec():
            return
        self.wtext.setText(dlg.selectedFiles()[0])

    def get_text(self):
        return self.wtext.text()


class ValidatedLineEdit(QLineEdit):
    __doc__ = ' http://snorf.net/blog/2014/08/09/using-qvalidator-in-pyqt4-to-validate-user-input/ '

    def __init__(self, validator, *args):
        super().__init__(*args)
        self.setValidator(validator)
        self.textChanged.connect(self.check_state)
        self.textChanged.emit(self.text())

    @pyqtSlot()
    def check_state(self, *args, **kwargs):
        sender = self.sender()
        validator = sender.validator()
        state = validator.validate(sender.text(), 0)[0]
        if state == QtGui.QValidator.Acceptable:
            color = '#c4df9b'
        else:
            if state == QtGui.QValidator.Intermediate:
                color = '#fff79a'
            else:
                color = '#f6989d'
        sender.setStyleSheet('QLineEdit { background-color: %s }' % color)


class MinuteSecondEdit(ValidatedLineEdit):

    def __init__(self, *args):
        regexp = QtCore.QRegExp('^(([0-9]?[0-9]:?)?[0-5][0-9]:?)?[0-5][0-9]$')
        validator = QtGui.QRegExpValidator(regexp)
        super().__init__(validator, *args)
        self.setValidator(validator)
        self.textChanged.connect(self.check_state)
        self.textChanged.emit(self.text())

    def get_time(self):
        t = self.text()
        if len(t) > 2:
            if ':' not in t:
                t = t[:-2] + ':' + t[-2:]
        if len(t) > 5:
            if ':' not in t[:-5]:
                t = t[:-5] + ':' + t[-5:]
        return t

    def get_h_m_s(self):
        t = self.get_time()
        if len(t) < 8:
            t = '00:00:00'[:8 - len(t)] + t
        h = int(t[0:2])
        m = int(t[3:5])
        s = int(t[6:8])
        return (h, m, s)


class BiggerMessageBox(QMessageBox):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setSizeGripEnabled(True)
        self.resize(self.sizeHint())

    def resizeEvent(self, event):
        result = super().resizeEvent(event)
        details_box = self.findChild(QtWidgets.QTextEdit)
        if details_box is not None:
            details_box.setFixedSize(details_box.sizeHint())
            details_box.setFixedSize(1000, 700)
        return result