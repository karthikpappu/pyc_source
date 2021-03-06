# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:\Anaconda2\lib\site-packages\pySAXS\guisaxs\qt\dlgModel.py
# Compiled at: 2018-09-26 09:12:11
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import pySAXS
from time import *
import sys
from pySAXS.tools import isNumeric
from pySAXS.tools import filetools
from pySAXS.guisaxs import dataset
from pySAXS.tools.isNumeric import *
from copy import copy
import numpy

class dlgModel(QtWidgets.QDialog):

    def __init__(self, parent, selectedData, type='model'):
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = uic.loadUi(pySAXS.UI_PATH + 'dlgModel.ui', self)
        self.parentwindow = parent
        self.selectedData = selectedData
        self.Model = parent.data_dict[selectedData].model
        self.par = self.Model.getArg()
        self.argbounds = self.Model.getArgBounds()
        self.itf = self.Model.getIstofit()
        self.qbase = copy(self.Model.q)
        self.ParDoc = []
        self.ParText = []
        self.MinText = []
        self.MaxText = []
        self.ParUncert = []
        self.SlideMax = 1000
        self.CheckFit = []
        self.slider = []
        self.fitexp = 0
        self.qmax = None
        self.backupArg = None
        self.type = type
        if self.type != 'model':
            self.qbase = self.parentwindow.data_dict[self.selectedData].q
        self.setWindowTitle(self.Model.Description)
        if self.type != 'model':
            p = self.parentwindow.data_dict[self.selectedData].parent
            if p[0] in self.parentwindow.data_dict:
                self.qmax = self.qbase[(-1)]
                qp = self.parentwindow.data_dict[p[0]].q
                self.qbase = qp
        self.constructUI()
        self.labelDatas.setText('')
        if self.type != 'model':
            self.labelDatas.setText(self.selectedData)
            if self.Model.prefit is not None:
                rawdata_name = self.parentwindow.data_dict[self.selectedData].rawdata_ref
                iexp = parent.data_dict[rawdata_name].i
                self.qbase = self.parentwindow.data_dict[self.selectedData].q
                self.par = self.Model.prefit(self.qbase, iexp)
                self.UpdateAfterFit(self.par)
        return

    def constructUI(self):
        """
        construct the UI
        """
        self.ui.labelDescription.setText(self.Model.Description)
        self.ui.labelAuthor.setText(self.Model.Author)
        for i in range(len(self.par)):
            item = QtWidgets.QLabel(self.ui.gbParameters)
            item.setText(self.Model.Doc[i] + ' : ')
            self.ui.gridParameters.addWidget(item, i + 1, 0, 1, 1)
            self.ParDoc.append(item)
            item = QtWidgets.QLineEdit(self.ui.gbParameters)
            item.setText(self.Model.Format[i] % self.par[i])
            self.ui.gridParameters.addWidget(item, i + 1, 1, 1, 1)
            item.textChanged.connect(self.onModelUpdate)
            item.setFixedWidth(75)
            self.ParText.append(item)
            item = QtWidgets.QLabel(self.ui.gbParameters)
            item.setText('-')
            item.setFixedWidth(150)
            item.setStyleSheet('color: blue')
            self.ui.gridParameters.addWidget(item, i + 1, 2, 1, 1)
            self.ParUncert.append(item)
            item = QtWidgets.QCheckBox(self.ui.gbParameters)
            item.setFixedWidth(20)
            item.setChecked(self.Model.istofit[i])
            self.ui.gridParameters.addWidget(item, i + 1, 3, 1, 1)
            self.ui.CheckFit.append(item)
            item = QtWidgets.QLineEdit(self.ui.gbParameters)
            if self.argbounds[i] is None:
                min = 0.0 * self.par[i]
            else:
                min = self.argbounds[i][0]
            item.setText(self.Model.Format[i] % min)
            item.setFixedWidth(75)
            self.ui.MinText.append(item)
            item.editingFinished.connect(self.onModelUpdate)
            self.ui.gridParameters.addWidget(item, i + 1, 4, 1, 1)
            item = QtWidgets.QLineEdit(self.ui.gbParameters)
            item.setFixedWidth(75)
            if self.argbounds[i] is None:
                max = 2.0 * self.par[i]
            else:
                max = self.argbounds[i][1]
            item.setText(self.Model.Format[i] % max)
            self.ui.MaxText.append(item)
            item.editingFinished.connect(self.onModelUpdate)
            self.ui.gridParameters.addWidget(item, i + 1, 5, 1, 1)

        qmin = self.qbase[0]
        qmax = self.qbase[(-1)]
        self.qminIndex = 0
        self.qmaxIndex = len(self.qbase) - 1
        self.ui.editQmin.setText('%6.5f' % qmin)
        self.ui.editQmax.setText('%6.5f' % qmax)
        self.ui.editQminVal.setText('%6.5f' % qmin)
        self.ui.editQmaxVal.setText('%6.5f' % qmax)
        self.ui.sliderQmin.setMinimum(0)
        self.ui.sliderQmax.setMinimum(0)
        self.ui.sliderQmin.setMaximum(self.qmaxIndex)
        self.ui.sliderQmax.setMaximum(self.qmaxIndex)
        self.ui.sliderQmin.setValue(0)
        self.ui.sliderQmax.setValue(self.qmaxIndex)
        self.ui.sliderQmin.valueChanged.connect(self.onSliderQminChange)
        self.ui.sliderQmax.valueChanged.connect(self.onSliderQmaxChange)
        self.ui.editQminVal.textChanged.connect(self.onQminEditChange)
        self.ui.editQmaxVal.textChanged.connect(self.onQmaxEditChange)
        choicelist = [
         'Normal', 'I/q', 'I/q^2', 'I/q^3', 'I/q^4', 'log(I)']
        self.radioList = []
        i = 0
        for choice in choicelist:
            item = QtWidgets.QRadioButton(self.ui.groupPlotExp)
            self.ui.gridLayoutPlotExp.addWidget(item, 0, i, 1, 1)
            item.setText(choice)
            self.ui.radioList.append(item)
            i += 1

        self.ui.radioList[0].setChecked(True)
        if self.type == 'model':
            self.ui.btnFit.setEnabled(False)
            self.ui.btnFitBounds.setEnabled(False)
            self.ui.groupPlotExp.setEnabled(False)
        else:
            self.ui.btnFit.setEnabled(True)
            self.ui.btnFitBounds.setEnabled(True)
            self.ui.groupPlotExp.setEnabled(True)
            self.ui.btnFit.clicked.connect(self.onFit)
            self.ui.btnFitBounds.clicked.connect(self.onFitBounds)
            self.ui.btnFitLMFIT.clicked.connect(self.onFitLMFIT)
            self.ui.btnBack.setEnabled(False)
            self.ui.btnBack.clicked.connect(self.onBack)
        self.ui.btnReport.clicked.connect(self.onReport)
        self.ui.btnCopy.clicked.connect(self.onCopy)
        self.ui.btnPaste.clicked.connect(self.onPaste)
        self.ui.lblChi.setStyleSheet('color: red')
        self.ui.lblChi.setText('-')
        return

    def onSliderQminChange(self, value):
        q = self.qbase[value]
        self.ui.editQmin.setText('%6.5f' % q)
        self.onModelUpdate()

    def onSliderQmaxChange(self, value):
        q = self.qbase[value]
        self.ui.editQmax.setText('%6.5f' % q)
        self.onModelUpdate()

    def onQminEditChange(self):
        if isNumeric(self.ui.editQminVal.text()):
            qmin = float(self.ui.editQminVal.text())
            try:
                self.ui.sliderQmin.setValue(numpy.where(self.qbase >= qmin)[0][0])
            except:
                pass

    def onQmaxEditChange(self):
        if isNumeric(self.ui.editQmaxVal.text()):
            qmax = float(self.ui.editQmaxVal.text())
            try:
                self.ui.sliderQmax.setValue(numpy.where(self.qbase <= qmax)[0][(-1)])
            except:
                pass

    def getPlotExp(self):
        for i in range(len(self.radioList)):
            if self.ui.radioList[i].isChecked():
                return i

        return 0

    def getValuesForm(self):
        """
        get the numeric vaules from the widget
        return True if sucess,
        return False if one value is not numeric
        """
        for i in range(len(self.Model.Arg)):
            if not isNumeric.isNumeric(str(self.ParText[i].text())):
                return

    def onModelUpdate(self, calculate=True):
        """
        when a parameter is updated
        """
        if not self.updateFit.isChecked():
            return
        else:
            if self.selectedData not in self.parentwindow.data_dict:
                self.parentwindow.printTXT(self.selectedData + ' dataset removed ? ')
                return
            self.bounds = []
            for i in range(len(self.Model.Arg)):
                if not isNumeric(str(self.ParText[i].text())):
                    return
                self.par[i] = float(eval(str(self.ParText[i].text())))
                self.itf[i] = self.CheckFit[i].isChecked()
                bmin = str(self.MinText[i].text())
                bmax = str(self.MaxText[i].text())
                self.bounds.append((bmin, bmax))

            self.Model.setIstofit(self.itf)
            self.Model.setArg(self.par)
            qmin = float(self.ui.editQmin.text())
            qmax = float(self.ui.editQmax.text())
            self.qminIndex = self.ui.sliderQmin.value()
            self.qmaxIndex = self.ui.sliderQmax.value()
            if self.qminIndex != 0 or self.qmaxIndex != len(self.qbase) - 1:
                self.Model.q = self.qbase[self.qminIndex:self.qmaxIndex]
            if not calculate:
                return
            if self.parentwindow.data_dict[self.selectedData].model is not None:
                self.parentwindow.data_dict[self.selectedData].model = self.Model
                self.parentwindow.data_dict[self.selectedData].i = self.Model.getIntensity()
                self.parentwindow.data_dict[self.selectedData].q = copy(self.Model.q)
                self.parentwindow.Replot()
            return

    def onFit(self):
        """
        user want to fit
        """
        self.ui.btnBack.setEnabled(True)
        self.backup()
        self.onModelUpdate(calculate=False)
        if self.selectedData not in self.parentwindow.data_dict:
            return
        else:
            rawdata_name = self.parentwindow.data_dict[self.selectedData].rawdata_ref
            self.parentwindow.printTXT('fit with raw data from ', rawdata_name)
            if rawdata_name in self.parentwindow.data_dict and self.parentwindow.data_dict[self.selectedData].model != None:
                if self.qminIndex != 0 or self.qmaxIndex != len(self.parentwindow.data_dict[rawdata_name].q) - 1:
                    q = self.parentwindow.data_dict[rawdata_name].q[self.qminIndex:self.qmaxIndex]
                    i = self.parentwindow.data_dict[rawdata_name].i[self.qminIndex:self.qmaxIndex]
                else:
                    q = self.parentwindow.data_dict[rawdata_name].q
                    i = self.parentwindow.data_dict[rawdata_name].i
                    self.Model.q = q
                self.fitexp = self.getPlotExp()
                res = self.Model.fit(i, self.fitexp)
                self.parentwindow.printTXT('fitted parameters : ', res)
                chi = self.Model.chi_carre(res, i)
                self.ui.lblChi.setText(str(chi))
                self.UpdateAfterFit(res)
            return

    def onCFit(self):
        """
        user want to fit
        """
        self.ui.btnBack.setEnabled(True)
        self.backup()
        self.onModelUpdate(calculate=False)
        if self.selectedData not in self.parentwindow.data_dict:
            return
        else:
            rawdata_name = self.parentwindow.data_dict[self.selectedData].rawdata_ref
            self.parentwindow.printTXT('fit with raw data from ', rawdata_name)
            if rawdata_name in self.parentwindow.data_dict and self.parentwindow.data_dict[self.selectedData].model != None:
                if self.qminIndex != 0 or self.qmaxIndex != len(self.parentwindow.data_dict[rawdata_name].q) - 1:
                    q = self.parentwindow.data_dict[rawdata_name].q[self.qminIndex:self.qmaxIndex]
                    i = self.parentwindow.data_dict[rawdata_name].i[self.qminIndex:self.qmaxIndex]
                else:
                    q = self.parentwindow.data_dict[rawdata_name].q
                    i = self.parentwindow.data_dict[rawdata_name].i
                    self.Model.q = q
                self.fitexp = self.getPlotExp()
                res = self.Model.cfit(i, self.fitexp)
                self.parentwindow.printTXT('fitted parameters : ', res)
                self.UpdateAfterFit(res)
            return

    def onFitBounds(self):
        self.ui.btnBack.setEnabled(True)
        self.backup()
        if self.selectedData not in self.parentwindow.data_dict:
            return
        else:
            self.onModelUpdate(calculate=False)
            rawdata_name = self.parentwindow.data_dict[self.selectedData].rawdata_ref
            self.parentwindow.printTXT('fit with raw data from ', rawdata_name)
            if rawdata_name in self.parentwindow.data_dict and self.parentwindow.data_dict[self.selectedData].model != None:
                if self.qminIndex != 0 or self.qmaxIndex != len(self.parentwindow.data_dict[rawdata_name].q) - 1:
                    q = self.parentwindow.data_dict[rawdata_name].q[self.qminIndex:self.qmaxIndex]
                    i = self.parentwindow.data_dict[rawdata_name].i[self.qminIndex:self.qmaxIndex]
                else:
                    q = self.parentwindow.data_dict[rawdata_name].q
                    i = self.parentwindow.data_dict[rawdata_name].i
                    self.Model.q = q
                res = self.Model.fitBounds(i, self.bounds, self.fitexp)
                self.parentwindow.printTXT('fitted parameters : ', res)
                self.UpdateAfterFit(res)
            return

    def onFitLMFIT(self):
        self.ui.btnBack.setEnabled(True)
        self.backup()
        if self.selectedData not in self.parentwindow.data_dict:
            return
        else:
            self.onModelUpdate(calculate=False)
            useError = self.ui.chkUseError.isChecked()
            rawdata_name = self.parentwindow.data_dict[self.selectedData].rawdata_ref
            if self.parentwindow.data_dict[rawdata_name].error is None:
                useError = False
            self.parentwindow.printTXT('fit with raw data from ', rawdata_name)
            if rawdata_name in self.parentwindow.data_dict and self.parentwindow.data_dict[self.selectedData].model != None:
                if self.qminIndex != 0 or self.qmaxIndex != len(self.parentwindow.data_dict[rawdata_name].q) - 1:
                    q = self.parentwindow.data_dict[rawdata_name].q[self.qminIndex:self.qmaxIndex]
                    i = self.parentwindow.data_dict[rawdata_name].i[self.qminIndex:self.qmaxIndex]
                    try:
                        error = self.parentwindow.data_dict[rawdata_name].error[self.qminIndex:self.qmaxIndex]
                    except:
                        useError = False

                else:
                    q = self.parentwindow.data_dict[rawdata_name].q
                    i = self.parentwindow.data_dict[rawdata_name].i
                    error = self.parentwindow.data_dict[rawdata_name].error
                    self.Model.q = q
                self.fitexp = self.getPlotExp()
                if useError:
                    self.parentwindow.printTXT('fit using data error ')
                    res, resLMFIT, uncertainties = self.Model.fitLMFIT(i, self.fitexp, err=error)
                else:
                    res, resLMFIT, uncertainties = self.Model.fitLMFIT(i, self.fitexp)
                self.parentwindow.printTXT('fitted parameters : ', res)
                chi = self.Model.chi_carre(res, i)
                self.ui.lblChi.setText(str(chi))
                self.UpdateAfterFit(res, resLMFIT, uncertainties)
            return

    def UpdateAfterFit(self, result, res_err=None, uncertainties=None):
        """
        update all after a fit
        """
        val = numpy.array(result).copy()
        for i in range(len(val)):
            self.ParText[i].setText(self.Model.Format[i] % val[i])
            if res_err is not None:
                if res_err[i] is not None:
                    try:
                        if val[i] != 0:
                            spercent = ('({0:.2%})').format(abs(res_err[i] / val[i]))
                        else:
                            spercent = ''
                    except ZeroDivisionError:
                        spercent = ''

                    self.ParUncert[i].setText(('+/-' + self.Model.Format[i] + ' %s') % (res_err[i], spercent))
                else:
                    self.ParUncert[i].setText('-')
            else:
                self.ParUncert[i].setText('-')

        self.parentwindow.data_dict[self.selectedData].model = self.Model
        self.parentwindow.data_dict[self.selectedData].i = self.Model.getIntensity()
        if uncertainties is not None:
            self.parentwindow.data_dict[self.selectedData].error = uncertainties
        self.parentwindow.Replot()
        self.ui.btnBack.setEnabled(True)
        self.onCopy()
        return

    def onReport(self):
        """
        display fit informations on the matplotlib graph
        """
        self.parentwindow.Replot()
        plotframe = self.parentwindow.plotframe
        reporttext = 'Model : ' + self.Model.Description + '\n'
        for i in range(len(self.par)):
            if str(self.ParUncert[i].text()) != '-':
                reporttext += self.Model.Doc[i] + ' : ' + str(self.ParText[i].text()) + ' ' + str(self.ParUncert[i].text()) + '\n'
            else:
                reporttext += self.Model.Doc[i] + ' : ' + str(self.ParText[i].text()) + '\n'

        reporttext += '\n' + ctime()
        plotframe.text(0.05, 0.05, reporttext)

    def onCopy(self):
        """
        copy parameters to clipboard
        """
        clipstring = ''
        self.clipboard = QtWidgets.QApplication.clipboard()
        for i in range(len(self.Model.Arg)):
            clipstring += str(self.ParText[i].text()) + ';'

        clipstring += str(self.ui.sliderQmin.value()) + ';'
        clipstring += str(self.ui.sliderQmax.value())
        self.clipboard.setText(clipstring)
        try:
            self.parentwindow.OnCopyModel(self.Model)
        except AttributeError:
            pass

    def onPaste(self, clip=None):
        """
        get parameters to clipboard
        """
        if clip is None:
            clip = QtWidgets.QApplication.clipboard()
        else:
            print clip
        clipboard = clip
        clipstring = str(clipboard.text())
        print clipstring
        if clipstring != '':
            l = clipstring.split(';')
            for i in range(len(l)):
                if i >= len(self.Model.Arg):
                    break
                if l[i] != '':
                    self.ParText[i].setText(l[i])

            if len(l) >= len(self.Model.Arg) + 2:
                if isNumeric.isNumeric(l[i]):
                    self.ui.sliderQmin.setValue(int(l[i]))
                if isNumeric.isNumeric(l[(i + 1)]):
                    self.ui.sliderQmax.setValue(int(l[(i + 1)]))
            self.onModelUpdate()
        return

    def backup(self):
        self.backupArg = []
        for a in self.Model.Arg:
            self.backupArg.append(a)

    def onBack(self):
        if self.backupArg is not None:
            for i in range(min([len(self.backupArg), len(self.Model.Arg)])):
                self.Model.Arg[i] = self.backupArg[i]
                self.ParText[i].setText(str(self.Model.Arg[i]))

            self.onModelUpdate()
        return