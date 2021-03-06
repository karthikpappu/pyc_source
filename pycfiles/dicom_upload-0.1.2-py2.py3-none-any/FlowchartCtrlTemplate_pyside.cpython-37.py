# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/flowchart/FlowchartCtrlTemplate_pyside.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 3175 bytes
from PySide import QtCore, QtGui

class Ui_Form(object):

    def setupUi(self, Form):
        Form.setObjectName('Form')
        Form.resize(217, 499)
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setVerticalSpacing(0)
        self.gridLayout.setObjectName('gridLayout')
        self.loadBtn = QtGui.QPushButton(Form)
        self.loadBtn.setObjectName('loadBtn')
        self.gridLayout.addWidget(self.loadBtn, 1, 0, 1, 1)
        self.saveBtn = FeedbackButton(Form)
        self.saveBtn.setObjectName('saveBtn')
        self.gridLayout.addWidget(self.saveBtn, 1, 1, 1, 2)
        self.saveAsBtn = FeedbackButton(Form)
        self.saveAsBtn.setObjectName('saveAsBtn')
        self.gridLayout.addWidget(self.saveAsBtn, 1, 3, 1, 1)
        self.reloadBtn = FeedbackButton(Form)
        self.reloadBtn.setCheckable(False)
        self.reloadBtn.setFlat(False)
        self.reloadBtn.setObjectName('reloadBtn')
        self.gridLayout.addWidget(self.reloadBtn, 4, 0, 1, 2)
        self.showChartBtn = QtGui.QPushButton(Form)
        self.showChartBtn.setCheckable(True)
        self.showChartBtn.setObjectName('showChartBtn')
        self.gridLayout.addWidget(self.showChartBtn, 4, 2, 1, 2)
        self.ctrlList = TreeWidget(Form)
        self.ctrlList.setObjectName('ctrlList')
        self.ctrlList.headerItem().setText(0, '1')
        self.ctrlList.header().setVisible(False)
        self.ctrlList.header().setStretchLastSection(False)
        self.gridLayout.addWidget(self.ctrlList, 3, 0, 1, 4)
        self.fileNameLabel = QtGui.QLabel(Form)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.fileNameLabel.setFont(font)
        self.fileNameLabel.setText('')
        self.fileNameLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.fileNameLabel.setObjectName('fileNameLabel')
        self.gridLayout.addWidget(self.fileNameLabel, 0, 1, 1, 1)
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate('Form', 'Form', None, QtGui.QApplication.UnicodeUTF8))
        self.loadBtn.setText(QtGui.QApplication.translate('Form', 'Load..', None, QtGui.QApplication.UnicodeUTF8))
        self.saveBtn.setText(QtGui.QApplication.translate('Form', 'Save', None, QtGui.QApplication.UnicodeUTF8))
        self.saveAsBtn.setText(QtGui.QApplication.translate('Form', 'As..', None, QtGui.QApplication.UnicodeUTF8))
        self.reloadBtn.setText(QtGui.QApplication.translate('Form', 'Reload Libs', None, QtGui.QApplication.UnicodeUTF8))
        self.showChartBtn.setText(QtGui.QApplication.translate('Form', 'Flowchart', None, QtGui.QApplication.UnicodeUTF8))


import widgets.TreeWidget as TreeWidget
import widgets.FeedbackButton as FeedbackButton