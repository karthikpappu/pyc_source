# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/bibolamazi_gui/qtauto/ui_filterinstanceeditor.py
# Compiled at: 2015-05-11 05:40:29
from PyQt4 import QtCore, QtGui
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:

    def _fromUtf8(s):
        return s


try:
    _encoding = QtGui.QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)


except AttributeError:

    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class Ui_FilterInstanceEditor(object):

    def setupUi(self, FilterInstanceEditor):
        FilterInstanceEditor.setObjectName(_fromUtf8('FilterInstanceEditor'))
        FilterInstanceEditor.resize(368, 361)
        self.gridLayout = QtGui.QGridLayout(FilterInstanceEditor)
        self.gridLayout.setObjectName(_fromUtf8('gridLayout'))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8('horizontalLayout'))
        self.label = QtGui.QLabel(FilterInstanceEditor)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName(_fromUtf8('label'))
        self.horizontalLayout.addWidget(self.label)
        self.cbxFilter = QtGui.QComboBox(FilterInstanceEditor)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cbxFilter.sizePolicy().hasHeightForWidth())
        self.cbxFilter.setSizePolicy(sizePolicy)
        self.cbxFilter.setEditable(True)
        self.cbxFilter.setInsertPolicy(QtGui.QComboBox.NoInsert)
        self.cbxFilter.setObjectName(_fromUtf8('cbxFilter'))
        self.horizontalLayout.addWidget(self.cbxFilter)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 2)
        self.lstOptions = QtGui.QTreeView(FilterInstanceEditor)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lstOptions.sizePolicy().hasHeightForWidth())
        self.lstOptions.setSizePolicy(sizePolicy)
        self.lstOptions.setVerticalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.lstOptions.setHorizontalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.lstOptions.setIndentation(0)
        self.lstOptions.setItemsExpandable(False)
        self.lstOptions.setAllColumnsShowFocus(True)
        self.lstOptions.setObjectName(_fromUtf8('lstOptions'))
        self.gridLayout.addWidget(self.lstOptions, 3, 0, 1, 2)
        self.hlytButtons = QtGui.QHBoxLayout()
        self.hlytButtons.setObjectName(_fromUtf8('hlytButtons'))
        self.btnFilterHelp = QtGui.QPushButton(FilterInstanceEditor)
        self.btnFilterHelp.setObjectName(_fromUtf8('btnFilterHelp'))
        self.hlytButtons.addWidget(self.btnFilterHelp)
        self.btnAddFavorite = QtGui.QToolButton(FilterInstanceEditor)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(':/pic/bookmark.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnAddFavorite.setIcon(icon)
        self.btnAddFavorite.setObjectName(_fromUtf8('btnAddFavorite'))
        self.hlytButtons.addWidget(self.btnAddFavorite)
        self.gridLayout.addLayout(self.hlytButtons, 4, 0, 1, 2)
        self.retranslateUi(FilterInstanceEditor)
        QtCore.QMetaObject.connectSlotsByName(FilterInstanceEditor)

    def retranslateUi(self, FilterInstanceEditor):
        FilterInstanceEditor.setWindowTitle(_translate('FilterInstanceEditor', 'Form', None))
        self.label.setText(_translate('FilterInstanceEditor', 'Filter:', None))
        self.btnFilterHelp.setText(_translate('FilterInstanceEditor', 'Help: Filter Reference', None))
        self.btnAddFavorite.setToolTip(_translate('FilterInstanceEditor', 'Add this full command line to your favorites', None))
        return


from . import bibolamazi_res_rc