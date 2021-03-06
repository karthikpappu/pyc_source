# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/gui/reconstruction/ftserie/h5editor/h5structseditor.py
# Compiled at: 2020-01-10 04:27:31
# Size of source mod 2**32: 15765 bytes
__author__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '08/06/2017'
from silx.gui import qt
from tomwer.core.process.reconstruction.ftseries.params.fastsetupdefineglobals import FastSetupAll
from tomwer.gui.linksqobject import LinkComboBox, LinkCheckBox, LinkLineEdit, LinkGroup
from tomwer.gui.utils.inputwidget import SelectionLineEdit
from tomwer.core.process.reconstruction.ftseries.params.reconsparams import _ReconsParam
from tomwer.core.process.reconstruction.ftseries.params.reconsparams import ReconsParams
from tomwer.core.process.reconstruction.ftseries.params.beamgeo import BeamGeoType
from tomwer.core.log import TomwerLogger
import enum
logger = TomwerLogger(__name__)

class H5StructsEditor:
    __doc__ = '\n    Abstract class which allow the edition of n H5 structures\n    '

    def __init__(self, structsManaged=None):
        self.defaultValues = {}
        self.dicVarToWidget = {}
        self.paramToWidget = {}
        self.structsManaged = {}
        self._isLoading = False
        if structsManaged is not None:
            assert type(structsManaged) in (list, tuple)
            for s in structsManaged:
                self.structsManaged[s] = {}
                self.defaultValues[s] = FastSetupAll.getDefaultValues(s)
                self.dicVarToWidget[s] = {}

        self.structs = self.structsManaged.keys()

    def isParamH5Managed(self, structID, paramID):
        return structID in self.structsManaged and paramID in self.structsManaged[structID]

    def linkComboboxWithH5Variable(self, qcombobox, structID, h5ParamName, fitwithindex=False, dic=None, filters=None, setDefault=True):
        """

        :param qcombobox: the QCombobox in the interface to edit/display the
            given h5ParamName
        :param h5ParamName: the parameter ID in the H5 structure.
        :param structID: the structID associated with the param ID
        :param fitwithindex: true if we want to store the index in the h5File,
            otherwise store the string
        :param filters: filter to apply on the string to get the requested
            value
        """
        assert type(qcombobox) is qt.QComboBox
        self.dicVarToWidget[structID][h5ParamName] = LinkComboBox(qcombobox, fitwithindex, dic, filters, setDefault)

    def linkCheckboxWithH5Variable(self, qcheckbox, structID, h5ParamName, invert=False):
        """

        :param qcheckbox: the QCheckBox in the interface to edit/display the
            given h5ParamName
        :param structID: the structID associated with the param ID
        :param h5ParamName: the parameter ID in the H5 structure.
        :param invert: true if we will not store the value state == checked but
            state == unchecked
        """
        assert type(qcheckbox) is qt.QCheckBox
        self.dicVarToWidget[structID][h5ParamName] = LinkCheckBox(qcheckbox, invert)

    def LinkLineEditWithH5Variable(self, qlineedit, structID, h5ParamName, h5paramtype=str):
        """

        :param qlineedit: the QLineEdit in the interface to edit/display the
            given h5ParamName
        :param h5ParamName: the parameter ID in the H5 structure.
        :param structID: the structID associated with the param ID
        :param h5ParamName: the parameter ID in the H5 structure.
        """
        assert type(qlineedit) is qt.QLineEdit
        self.dicVarToWidget[structID][h5ParamName] = LinkLineEdit(qlineedit, h5paramtype)

    def LinkSelectionLineEditWithH5Variable(self, qlineedit, structID, h5ParamName, h5paramtype=str):
        """

        :param qlineedit: the QLineEdit in the interface to edit/display the
            given h5ParamName
        :param h5ParamName: the parameter ID in the H5 structure.
        :param structID: the structID associated with the param ID
        :param h5ParamName: the parameter ID in the H5 structure.
        """
        assert isinstance(qlineedit, SelectionLineEdit)
        self.dicVarToWidget[structID][h5ParamName] = LinkLineEdit(qlineedit, h5paramtype)

    def linkGroupWithH5Variable(self, group, structID, h5ParamName, getter, setter):
        self.dicVarToWidget[structID][h5ParamName] = LinkGroup(group, getter, setter)

    def getParamValue(self, structID, paramID):
        if not self.isParamH5Managed(structID, paramID):
            return
        return self._getParamValue(self, structID, paramID)

    def _getParamValue(self, structID, h5ParamName):
        """Return the value for the stored h5ParamName

        :param str structID: ID of the h5 group
        :param h5ParamName: the name of the parameter we want to get the value for
        """
        if structID not in self.dicVarToWidget:
            mess = 'cannot find structur %s in the managed structure ' % structID
            logger.error(mess)
            return
        if h5ParamName not in self.dicVarToWidget[structID]:
            mess = 'cannot find parameter %s in the stored parameters.' % h5ParamName
            logger.error(mess)
            return
        link = self.dicVarToWidget[structID][h5ParamName]
        if type(link) is LinkComboBox:
            return self._getQComboboxValue(link)
        if type(link) is LinkLineEdit:
            return self._getQLineEditValue(link)
        if type(link) is LinkCheckBox:
            return self._getQCheckBoxValue(link)
        if type(link) is LinkGroup:
            return link.getter()
        mess = 'type of the LinkQObject (%s) is not managed by H5StructEditor' % type(link)
        raise ValueError(mess)

    def getStructs(self):
        """

        :return: the struct represented by the object under the tuple
                 (structID, structParameters)
        """
        res = {}
        for structID in self.dicVarToWidget:
            parameters = {}
            for param in self.dicVarToWidget[structID]:
                parameters[param] = self._getParamValue(structID, param)

            res[structID] = parameters

        return res

    def load(self, allStructs):
        """
        Set the parameters values to corresponding QObject.

        :param allStructs: is the H5file set of parameters. In this case it
                           include nodes FT, PAGANIN...
        """
        if self._isLoading is True:
            return
        else:
            assert isinstance(allStructs, _ReconsParam)
            self._isLoading = True
            self.defaults = None
            if isinstance(allStructs, ReconsParams):
                for structID in self.structs:
                    self.structsManaged[structID] = []
                    if structID not in allStructs.all_params:
                        error = structID + " is not in the given structure. Can't load."
                        error += 'Will load the default structure'
                        logger.error(error)
                        recons_param = self.defaultValues[structID]
                    else:
                        recons_param = allStructs._get_parameter_value(structID)
                    if not recons_param is None:
                        assert isinstance(recons_param, (_ReconsParam, _ReconsParam))
                    for param in self.dicVarToWidget[structID]:
                        self.structsManaged[structID].append(param)
                        paramValue = recons_param._get_parameter_value(param)
                        assert type(paramValue) is not dict
                        self.setParam(structID, param, paramValue=paramValue)

            else:
                for structID in self.structsManaged:
                    self.structsManaged[structID] = []
                    for param in self.dicVarToWidget[structID]:
                        self.structsManaged[structID].append(param)
                        paramValue = allStructs[param]
                        assert not isinstance(paramValue, _ReconsParam)
                        self.setParam(structID, param, paramValue=paramValue)

        if hasattr(self, '_sliceSlectionWidget'):
            self._sliceSlectionWidget.setEnabled(self._recons_params.do_test_slice)
        self._isLoading = False

    def setParam(self, structID, param, paramValue):
        """Set the parameter value for the gicen H5StructEditor param name

        :param str structID: ID of the h5 group
        :param param: ID of the H5 parameter to set
        :param paramValue: the value to set to the given parameter
        """
        if not structID in self.dicVarToWidget:
            raise AssertionError
        else:
            assert param in self.dicVarToWidget[structID]
            if type(self.dicVarToWidget[structID][param]) is LinkLineEdit:
                self.dicVarToWidget[structID][param].qobject.setText(str(paramValue))
            else:
                if type(self.dicVarToWidget[structID][param]) is LinkCheckBox:
                    if self.dicVarToWidget[structID][param].invert is False:
                        state = qt.Qt.Checked if bool(paramValue) else qt.Qt.Unchecked
                    else:
                        state = qt.Qt.Unchecked if bool(paramValue) else qt.Qt.Checked
                    self.dicVarToWidget[structID][param].qobject.setCheckState(state)
                else:
                    if type(self.dicVarToWidget[structID][param]) is LinkComboBox:
                        self._setQComboboxValue(structID, param, paramValue)
                    else:
                        if type(self.dicVarToWidget[structID][param]) is LinkGroup:
                            if self.dicVarToWidget[structID][param].setter is not None:
                                self.dicVarToWidget[structID][param].setter(paramValue)
                        else:
                            message = 'parameter %s no managed' % param
                            logger.warning(message)

    def _getQComboboxValue(self, link):
        """
        Return the actual value saved in the GUI
        """
        assert type(link) is LinkComboBox
        value = link.qobject.currentIndex() if link.fitwithindex else link.qobject.currentText()
        if link.filters is not None:
            for filt in link.filters:
                value = value.replace(filt, '')

        if link.dicCBtoH5 is not None:
            assert value in link.dicCBtoH5
            return link.dicCBtoH5[value]
        return value

    def _getValueToSetFromDic(self, structID, param, paramValue):
        if isinstance(paramValue, BeamGeoType):
            paramValue = paramValue.name[0]
        elif self.dicVarToWidget[structID][param].dicH5ToCB is not None:
            if paramValue not in self.dicVarToWidget[structID][param].dicH5ToCB:
                error = "'%s' is not a correct value for %s." % (paramValue, param)
                error += ' Setting to default'
                logger.warning(error)
                return self.dicVarToWidget[structID][param].dicH5ToCB[self.getDefaultValue(structID, param)]
            return self.dicVarToWidget[structID][param].dicH5ToCB[paramValue]
        else:
            return paramValue

    def _setQComboboxValue(self, structID, param, paramValue):
        """
        Set the value of the QCombobox for the param param of the struct
        StructID

        :param str structID: ID of the h5 group
        :param param: the H5parameter we want to store for setting the
            reconstruction
        :param paramValue: Value of param
        """
        finalParamValue = self._getValueToSetFromDic(structID, param, paramValue)
        if isinstance(finalParamValue, BeamGeoType):
            finalParamValue = finalParamValue.name[0]
        else:
            if isinstance(finalParamValue, enum.Enum):
                finalParamValue = finalParamValue.name
        index = self.dicVarToWidget[structID][param].qobject.findText(finalParamValue)
        if index is -1:
            info = '(Loading H5StructEditor) :'
            info += 'For parameter %s' % param
            info += ', value %s not existing yet.' % finalParamValue
            info += "Adding 'unregular value. "
            info += 'Can be source of error.'
            logger.info(info)
            index = self.dicVarToWidget[structID][param].qobject.count()
            self.dicVarToWidget[structID][param].qobject.addItem(str(finalParamValue))
        self.dicVarToWidget[structID][param].qobject.setCurrentIndex(index)

    def _getQLineEditValue(self, link):
        assert type(link) is LinkLineEdit
        if link.h5paramtype is int:
            return link.h5paramtype(float(link.qobject.text()))
        return link.h5paramtype(link.qobject.text())

    def _getQCheckBoxValue(self, link):
        assert type(link) is LinkCheckBox
        checked = link.qobject.isChecked()
        return int(not checked if link.invert else checked)

    def getDefaultValue(self, structID, param):
        """
        :return: the default parameter value or None if not existing
        """
        if structID not in self.defaultValues:
            error = '%s structure is not registred in the default parameters.' % structID
            raise ValueError(error)
        if param not in self.defaultValues[structID]:
            error = '%s parameter is not registred in the default parameters.' % param
            error += "Shouldn't be managed by H5StructEditor"
            raise ValueError(error)
        return self.defaultValues[structID]._get_parameter_value(param)

    def clear(self):
        self.paramToWidget.clear()
        self.structsManaged.clear()
        self.dicVarToWidget.clear()