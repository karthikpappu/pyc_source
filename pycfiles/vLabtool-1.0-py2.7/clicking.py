# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/vLabtool/widgets/clicking.py
# Compiled at: 2015-06-20 06:13:25
import sip, os
os.environ['QT_API'] = 'pyqt'
sip.setapi('QString', 2)
sip.setapi('QVariant', 2)
from PyQt4 import QtCore, QtGui
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Form(object):

    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8('Form'))
        Form.resize(300, 31)
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8('verticalLayout'))
        self.frame = QtGui.QFrame(Form)
        self.frame.setFrameShape(QtGui.QFrame.Box)
        self.frame.setFrameShadow(QtGui.QFrame.Sunken)
        self.frame.setLineWidth(2)
        self.frame.setObjectName(_fromUtf8('frame'))
        self.horizontalLayout = QtGui.QHBoxLayout(self.frame)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8('horizontalLayout'))
        self.button = QtGui.QPushButton(self.frame)
        self.button.setObjectName(_fromUtf8('button'))
        self.horizontalLayout.addWidget(self.button)
        self.label = QtGui.QLabel(self.frame)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8('label'))
        self.horizontalLayout.addWidget(self.label)
        self.verticalLayout.addWidget(self.frame)
        self.retranslateUi(Form)
        QtCore.QObject.connect(self.button, QtCore.SIGNAL(_fromUtf8('clicked()')), Form.clicked)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate('Form', 'Form', None, QtGui.QApplication.UnicodeUTF8))
        self.button.setText(QtGui.QApplication.translate('Form', 'Push', None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate('Form', 'Results', None, QtGui.QApplication.UnicodeUTF8))
        return