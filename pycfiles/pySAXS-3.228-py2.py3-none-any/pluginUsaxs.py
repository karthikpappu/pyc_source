# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\winpython\python-2.7.10.amd64\lib\site-packages\pySAXS\guisaxs\qt\pluginUsaxs.py
# Compiled at: 2016-02-29 04:24:26
from PyQt4 import QtGui, QtCore
import guidata
from guidata.dataset import datatypes
from guidata.dataset import dataitems
import numpy
from pySAXS.LS import LSusaxs
from pySAXS.guisaxs.dataset import *
from pySAXS.guisaxs.qt import plugin
classlist = ['USAXSTransmission', 'USAXSDesmearing']

class USAXSTransmission(plugin.pySAXSplugin):
    menu = 'Data Treatment'
    subMenu = 'USAXS'
    subMenuText = 'Background and Data correction'
    icon = 'hist.png'
    wavelength = 1.54189

    def execute(self):
        """
        The user click on "USAXS - Data correction"
        """
        if self.selectedData is None:
            QtGui.QMessageBox.information(self.parent, 'pySAXS', 'No data are selected', buttons=QtGui.QMessageBox.Ok, defaultButton=QtGui.QMessageBox.NoButton)
            return
        else:
            if not self.data_dict.has_key('rock'):
                QtGui.QMessageBox.information(self.parent, 'pySAXS', "Load data and rocking curve before correcting by transmission \n            (Try to rename the rocking curve datas in 'rock')", buttons=QtGui.QMessageBox.Ok, defaultButton=QtGui.QMessageBox.NoButton)
                return
            rocklist = [
             'rock']
            rocklist += self.ListOfDatasChecked()
            items = {'wavelength': dataitems.FloatItem('Wavelength', self.wavelength), 
               'backgroundData': dataitems.FloatItem('Background data :', 0.0, unit='cps/s'), 
               'backgroundRC': dataitems.FloatItem('Background Rocking curve :', 0.0, unit='cps/s'), 
               'shiftdata': dataitems.FloatItem('Shift Data :', 0.0, unit='steps'), 
               'shiftrock': dataitems.FloatItem('Shift Rocking curve :', 0.0, unit='steps'), 
               'qmin': dataitems.FloatItem('q min after substraction :', 0.0003), 
               'keepdatacentered': dataitems.BoolItem('Keep intermediary centered datas', False), 
               'rock': dataitems.ChoiceItem('Rocking curve :', rocklist), 
               'desmearing': dataitems.BoolItem('Continue with desmearing ?', False)}
            clz = type('Transmission and Data correction :', (datatypes.DataSet,), items)
            self.form = clz()
            if self.form.edit():
                self.calculate()
            return

    def calculate(self):
        """
        do the transmission correction after dialog box 
        """
        self.printTXT('-----USAXS Data correction --------')
        self.printTXT('Thickness is fixed at 1')
        self.thick = 1
        self.steprock = self.form.shiftrock
        self.stepexp = self.form.shiftdata
        self.backgrdData = self.form.backgroundData
        self.backgrdRC = self.form.backgroundRC
        self.wavelength = self.form.wavelength
        keepcentered = False
        keepcentered = self.form.keepdatacentered
        desmearing = self.form.desmearing
        print 'desmearing ?', desmearing
        qminimum = self.form.qmin
        n = 15
        a1 = 10000.0
        a2 = 1e-10
        it = 2000
        tol = 1e-15
        Iexp = self.data_dict[self.selectedData].i - self.backgrdData
        qexp = self.data_dict[self.selectedData].q
        Irock = self.data_dict['rock'].i - self.backgrdRC
        qrock = self.data_dict['rock'].q
        a0exp = Iexp[numpy.argmax(Iexp)]
        a0rock = Irock[numpy.argmax(Irock)]
        Thetaexp = qexp
        Thetarock = qrock
        Fitexp, Thetaexp_sel, Iexp_sel, FitParamexp = LSusaxs.FitGauss(Thetaexp, Iexp, n, a0exp, a1, a2, tol, it)
        Fitrock, Thetarock_sel, Irock_sel, FitParamrock = LSusaxs.FitGauss(Thetarock, Irock, n, a0rock, a1, a2, tol, it)
        self.printTXT('Data center found at ', FitParamexp[2])
        self.printTXT('RC center found at ', FitParamrock[2])
        DeltaThetaexp = -FitParamexp[2]
        DeltaThetarock = -FitParamrock[2]
        shiftexp = abs(Thetaexp_sel[0] - Thetaexp_sel[1])
        shiftrock = abs(Thetarock_sel[0] - Thetarock_sel[1])
        NewThetaexp_sel = LSusaxs.Qscalemod(DeltaThetaexp, Thetaexp_sel, self.stepexp * shiftexp)
        NewThetarock_sel = LSusaxs.Qscalemod(DeltaThetarock, Thetarock_sel, self.steprock * shiftrock)
        CorrThetaexp_positive = numpy.repeat(NewThetaexp_sel, NewThetaexp_sel > 0.0)
        Iexp_sel_positive = numpy.repeat(Iexp_sel, NewThetaexp_sel > 0.0)
        qnewexp = LSusaxs.Qscalemod(DeltaThetaexp, Thetaexp, self.stepexp * shiftexp)
        qnewrock = LSusaxs.Qscalemod(DeltaThetarock, Thetarock, self.steprock * shiftexp)
        if keepcentered:
            self.data_dict[self.selectedData + ' centered'] = dataset(self.selectedData + ' centered', qnewexp, Iexp, 'centered datas', type='calculated', parent=[self.selectedData])
            self.data_dict['rock centered'] = dataset('rock centered', qnewrock, Irock, 'rock datas', type='calculated', parent=['rock'])
        self.printTXT('max value for experimental datas : ', FitParamexp[0])
        self.printTXT('max value for rocking curve datas : ', FitParamrock[0])
        self.TransmissionValue = FitParamexp[0] / FitParamrock[0]
        self.printTXT('Transmission of the sample (%)= ', self.TransmissionValue)
        self.printTXT('Sample thickness (cm.)=', self.thick)
        qnewpos = numpy.repeat(qnewrock, qnewrock >= 0.0)
        Inewpos = numpy.repeat(Irock, qnewrock >= 0.0)
        self.printTXT('minimum Theta taken for central beam calculation= ', qnewpos[0])
        thetanewpos = LSusaxs.QtoTheta(qnewpos, self.wavelength)
        sommetheta = 2.0 * LSusaxs.somme(thetanewpos, Inewpos)
        self.printTXT('Central beam area(counts.s^-1.rad^-2)= ', sommetheta)
        qnew, ITcorr = LSusaxs.TrCorrectedProf(qnewexp, Iexp, qnewrock, Irock, self.thick, sommetheta, self.TransmissionValue)
        newname = self.selectedData + ' substracted'
        self.data_dict[newname] = dataset(newname, numpy.repeat(qnew, qnew > qminimum), numpy.repeat(ITcorr, qnew > qminimum), 'substracted datas', type='scaled', parent=[
         self.selectedData])
        self.redrawTheList()
        self.Replot()
        if desmearing:
            desmear = USAXSDesmearing(self.parent, self.selectedData + ' substracted', noGUI=True)
            desmear.setParameters({'ExtrapolationType': LSusaxs.POWERLAW})
            desmear.execute()


class USAXSDesmearing(plugin.pySAXSplugin):
    """
    class for desmearing USAXS
    """
    menu = 'Data Treatment'
    subMenu = 'USAXS'
    subMenuText = 'Desmearing'
    icon = 'find.png'

    def execute(self):
        """
        The user click on "USAXS - Data correction"
        """
        if self.selectedData is None:
            QtGui.QMessageBox.information(self.parent, 'pySAXS', 'No data are selected', buttons=QtGui.QMessageBox.Ok, defaultButton=QtGui.QMessageBox.NoButton)
            return
        else:
            if not self.data_dict.has_key('resfunc'):
                QtGui.QMessageBox.information(self.parent, 'pySAXS', "Load resolution function before deconvolution \n            (or rename  in 'resfunc')", buttons=QtGui.QMessageBox.Ok, defaultButton=QtGui.QMessageBox.NoButton)
                return
            self.printTXT('-----USAXS desmearing --------')
            resx = self.data_dict['resfunc'].q
            resy = self.data_dict['resfunc'].i
            if not self.noGUI:
                self.typeList = (LSusaxs.POWERLAW, LSusaxs.CONSTANTBACKGROUND)
                items = {'ExtrapolationType': dataitems.ChoiceItem('Type of extrapolation for high q', self.typeList)}
                clz = type('USAXS Desmearing :', (datatypes.DataSet,), items)
                self.form = clz()
                if not self.form.edit():
                    return
                print self.form.ExtrapolationType
                self.ExtrapolationType = self.form.ExtrapolationType
            self.printTXT('Extrapolation type : ', self.ExtrapolationType)
            it = 3
            ns = 1
            self.wavelength = 1.54189
            Isous = self.data_dict[self.selectedData].i
            qsous = self.data_dict[self.selectedData].q
            theta = LSusaxs.QtoTheta(qsous, self.wavelength)
            Idec = LSusaxs.lake(theta, Isous, it, self.ExtrapolationType, ns, resx=resx, resy=resy)
            qdec = qsous
            self.data_dict[self.selectedData + ' deconvoluted'] = dataset(self.selectedData + ' deconvoluted', qdec, Idec, self.selectedData + 'deconvoluted', True, type='calculated', parent=[self.selectedData])
            self.redrawTheList()
            self.Replot()
            return