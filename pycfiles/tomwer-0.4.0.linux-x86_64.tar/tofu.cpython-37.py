# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/gui/reconstruction/lamino/tofu/tofu.py
# Compiled at: 2019-08-19 02:52:33
# Size of source mod 2**32: 17308 bytes
"""Some widget construction to check if a sample moved"""
__author__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '01/06/2018'
from silx.gui import qt
from silx.io import dictdump
from tomwer.core.log import TomwerLogger
from tomwer.core.process.reconstruction.lamino.tofu import SCAN_TYPES, SCAN_TYPES_I, FFCWhen
from tomwer.core.process.reconstruction.lamino.tofu import _retrieve_opts_recons_cmd
from tomwer.core.utils.char import PSI_CHAR
from tomwer.gui import icons
from tomwer.gui.reconstruction.lamino.tofu import settings
from .TofuOptionLoader import _TofuOptionLoader, _getterSetter
from .projections import InputProjectionsScrollArea
from .tofuexpert import ExpertTofuWidget
from .tofuoutput import OutputTofuWidget
_logger = TomwerLogger(__name__)

class TofuWindow(qt.QMainWindow):
    __doc__ = '\n    Widget used to interface lamino reconstruction using tofu\n    '

    def __init__(self, parent):
        qt.QMainWindow.__init__(self, parent)
        self.setWindowFlags(qt.Qt.Widget)
        self._mainWidget = TofuWidget(parent=self)
        self.setCentralWidget(self._mainWidget)
        self.save = self._mainWidget.save
        self.load = self._mainWidget.load
        self.loadFromScan = self._mainWidget.loadFromScan
        self.getParameters = self._mainWidget.getParameters
        self.setParameters = self._mainWidget.setParameters
        self.getAdditionalRecoOptions = self._mainWidget.getAdditionalRecoOptions
        self.setAdditionalRecoOptions = self._mainWidget.setAdditionalRecoOptions
        self.getAdditionalPreprocessOptions = self._mainWidget.getAdditionalPreprocessOptions
        self.setAdditionalPreprocessOptions = self._mainWidget.setAdditionalPreprocessOptions
        self.removeOutputDir = self._mainWidget.removeOutputDir
        self.setRemoveOutputDir = self._mainWidget.setRemoveOutputDir
        style = qt.QApplication.style()
        saveIcon = style.standardIcon(qt.QStyle.SP_DialogSaveButton)
        self._saveAction = qt.QAction(saveIcon, 'save', self)
        self._saveAction.setToolTip('save configuration')
        self._saveAction.setShortcut(qt.QKeySequence.Save)
        self.menuBar().addAction(self._saveAction)
        self._saveAction.triggered.connect(self.save)
        loadIcon = style.standardIcon(qt.QStyle.SP_DialogOpenButton)
        self._loadAction = qt.QAction(loadIcon, 'load', self)
        self._loadAction.setToolTip('load configuration')
        self._loadAction.setShortcut(qt.QKeySequence.Open)
        self.menuBar().addAction(self._loadAction)
        self._loadAction.triggered.connect(self.load)


class TofuWidget(_TofuOptionLoader, qt.QWidget):
    _OPT_RECO_SECTION_ID = 'options_reco'
    _OPT_PREPROCESS_SECTION_ID = 'options_preprocess'
    _TOMWER_CONFIG = 'tomwer_configuration'

    def __init__(self, parent):
        qt.QWidget.__init__(self, parent)
        self.setLayout(qt.QVBoxLayout())
        self._scanTypeWidget = ScanTypeWidget(parent=self)
        self.layout().addWidget(self._scanTypeWidget)
        self._tabs = _TofuTab(parent=self)
        self.layout().addWidget(self._tabs)
        _TofuOptionLoader.__init__(self, options={'z-parameter': _getterSetter(getter=(self._scanTypeWidget.getScanType), setter=(self._scanTypeWidget.setScanType))},
          childs=[
         self._tabs])
        self.getAdditionalRecoOptions = self._tabs.getAdditionalRecoOptions
        self.getAdditionalPreprocessOptions = self._tabs.getAdditionalPreprocessOptions
        self.removeOutputDir = self._tabs._outputWidget._outputWidget.removeIfExist
        self.setRemoveOutputDir = self._tabs._outputWidget._outputWidget.setRemoveIfExist
        self._scanTypeWidget._scanType.currentIndexChanged.connect(self._scanTypeChanged)
        self._tabs._outputWidget._volumeAngleGrp._grpPlane.sigPlaneChanged.connect(self._scanTypeChanged)
        self._scanTypeChanged()

    def _scanTypeChanged(self, *args, **kwargs):
        scan_type = self._scanTypeWidget._scanType.currentText()
        x_center = 0
        if scan_type == 'slice stack':
            _type = '(pixel)'
            _range = (
             -settings.SLICE_STACK_RANGE_HS, settings.SLICE_STACK_RANGE_HS)
            _step_size = settings.SLICE_STACK_STEP_SIZE
            _nb_slices = settings.SLICE_STACK_NB_SLICES
        else:
            if scan_type == 'rotation center':
                _type = '(pixel)'
                x_center = self._tabs._inputWidget.centeringWidget.getXCenter()
                _range = (x_center - settings.ROT_CENTER_RANGE_HS,
                 x_center + settings.ROT_CENTER_RANGE_HS)
                _step_size = settings.ROT_CENTER_STEP_SIZE
                _nb_slices = settings.ROT_CENTER_NB_SLICES
            else:
                if scan_type == 'lamino angle':
                    _type = '(degree)'
                    lamino_angle = self._tabs._inputWidget.rotationAngle.getLaminoAngle()
                    x_center = lamino_angle
                    _range = (lamino_angle - settings.LAMINO_ANG_RANGE_HS,
                     lamino_angle + settings.LAMINO_ANG_RANGE_HS)
                    _step_size = settings.LAMINO_ANG_STEP_SIZE
                    _nb_slices = settings.LAMINO_ANG_NB_SLICES
                else:
                    if scan_type == PSI_CHAR + ' angle':
                        _type = '(degree)'
                        psi_angle = self._tabs._inputWidget.rotationAngle.getPsiAngle()
                        x_center = psi_angle
                        _range = (
                         -settings.PSI_ANG_RANGE_HS, settings.PSI_ANG_RANGE_HS)
                        _step_size = settings.PSI_ANG_STEP_SIZE
                        _nb_slices = settings.PSI_ANG_NB_SLICES
                    else:
                        raise NotImplementedError('')
        _stepSizeAndRangeWidget = self._tabs._outputWidget._stepSizeAndRange
        _stepSizeAndRangeWidget._setStepSizeType(_type)
        _stepSizeAndRangeWidget._z_label.setVisible(scan_type == 'slice stack')
        _stepSizeAndRangeWidget._zSB.setVisible(scan_type == 'slice stack')
        _stepSizeAndRangeWidget.setRegion(region=(_range[0], _range[1], _step_size))
        _stepSizeAndRangeWidget._setXCenter(x_center)
        _stepSizeAndRangeWidget.setNCut(_nb_slices)
        if scan_type == PSI_CHAR + ' angle':
            scan_type = 'psi angle'
        self._tabs._outputWidget._setScanType(scan_type)

    def load(self):
        dialog = qt.QFileDialog(self)
        dialog.setNameFilters(['ini (*.ini)'])
        dialog.setFileMode(qt.QFileDialog.ExistingFile)
        if not dialog.exec_():
            dialog.close()
            return
        self.loadFile(dialog.selectedFiles()[0])

    def loadFile(self, _file):
        _logger.info(('loading', _file))
        try:
            conf = dictdump.load(_file)
        except Exception as error:
            try:
                _logger.warning('Fail to load configuration from ', _file, '. Reason is', error)
            finally:
                error = None
                del error

        else:
            if self._OPT_RECO_SECTION_ID not in conf:
                _logger.warning('Dict load is not recognized. Fail to load configuration')
                reco_opts = {}
            else:
                reco_opts = conf[self._OPT_RECO_SECTION_ID]
            if self._OPT_PREPROCESS_SECTION_ID not in conf:
                _logger.warning('Dict load is not recognized. Fail to load configuration')
                preprocess_opts = {}
            else:
                preprocess_opts = conf[self._OPT_PREPROCESS_SECTION_ID]
            if self._TOMWER_CONFIG not in conf:
                _logger.warning('Dict load is not recognized. Fail to load configuration')
                tomwer_config = {}
            else:
                tomwer_config = conf[self._TOMWER_CONFIG]
            self.setConfigFromOptionsDict(reco_opts=reco_opts, preprocess_opts=preprocess_opts,
              tomwer_config=tomwer_config)

    def save(self):
        dialog = qt.QFileDialog(self)
        dialog.setNameFilters(['ini (*.ini)'])
        dialog.setAcceptMode(qt.QFileDialog.AcceptSave)
        dialog.setFileMode(qt.QFileDialog.AnyFile)
        if not dialog.exec_():
            dialog.close()
            return
        self.saveTo(dialog.selectedFiles()[0])

    def saveTo(self, _file):
        """Save the parameters used for reconstruction into an ini file"""
        if _file.lower().endswith('.ini') is False:
            _file = _file + '.ini'
        _logger.info(('saving to', _file))
        fixedOptions = self.getParameters()
        additionalRecoOptions = self.getAdditionalRecoOptions()
        additionalPreprocessOptions = self.getAdditionalPreprocessOptions()
        pre_proc_ffc = fixedOptions['ffc-when']
        if type(pre_proc_ffc) is str:
            pre_proc_ffc = getattr(FFCWhen, pre_proc_ffc)
        assert isinstance(pre_proc_ffc, FFCWhen)

        def store(options, key, ddict):
            optionsList = _retrieve_opts_recons_cmd(scan_id=None, recons_param=fixedOptions,
              additional_opts=options,
              pre_proc_ffc=(pre_proc_ffc is FFCWhen.preprocessing))
            optionsList = optionsList.split('--')
            optionsDict = {}
            for opt in optionsList:
                if opt == ' ':
                    continue
                else:
                    _opt = opt.lstrip(' ')
                    if '=' in _opt:
                        optName, value = _opt.split('=', 1)
                        value = value.replace('=', '')
                    else:
                        if ' ' in _opt:
                            optName, value = _opt.split(' ', 1)
                            value = value.replace(' ', '')
                        else:
                            optName = _opt
                            value = ''
                optName = optName.rstrip(' ')
                optionsDict[optName] = value

            ddict[key] = optionsDict

        ddict = {}
        store(options=additionalRecoOptions, key=(self._OPT_RECO_SECTION_ID), ddict=ddict)
        store(options=additionalPreprocessOptions, key=(self._OPT_PREPROCESS_SECTION_ID), ddict=ddict)
        config_dict = {'rm-tif':fixedOptions['rm-tif'], 
         'ffc-when':fixedOptions['ffc-when'], 
         'half-acquisition':fixedOptions['half-acquisition'], 
         'blend':fixedOptions['blend'], 
         'adjust-mean':fixedOptions['adjust-mean'], 
         'z':fixedOptions['z']}
        ddict[self._TOMWER_CONFIG] = config_dict
        dictdump.dicttoini(ddict=ddict, inifile=_file)

    def setConfigFromOptionsDict(self, reco_opts, preprocess_opts, tomwer_config):
        """
        extract from the command line the list of option names and their
        values if any to store them

        :param list or tuple options:
        """
        self._tabs._expertWidget.resetAdditionalRecoOptions()
        self._tabs._expertWidget.resetAdditionalPreprocessOptions()
        add_options = self.setParameters(reco_opts)
        for option, optValue in add_options.items():
            self._tabs._expertWidget.addAdditionalRecoOption(option=option, value=optValue)

        add_options = self.setParameters(preprocess_opts)
        for option, optValue in add_options.items():
            self._tabs._expertWidget.addAdditionalPreprocessOption(option=option, value=optValue)

        if 'rm-tif' in tomwer_config:
            self._tabs._outputWidget.setRemoveTiff(tomwer_config['rm-tif'])
        if 'half-acquisition' in tomwer_config:
            self._tabs._inputWidget.setHalfAcquisition(tomwer_config['half-acquisition'])
        if 'ffc-when' in tomwer_config:
            self._tabs._inputWidget.setWhenApplyFFC(tomwer_config['ffc-when'])
        if 'blend' in tomwer_config:
            self._tabs._inputWidget.setBlend(tomwer_config['blend'])
        if 'adjust-mean' in tomwer_config:
            self._tabs._inputWidget.setAdjustMean(tomwer_config['adjust-mean'])
        if 'z' in tomwer_config:
            self._tabs._outputWidget.setZ(tomwer_config['z'])

    def setAdditionalRecoOptions(self, options):
        assert isinstance(options, str)
        self._tabs._expertWidget.resetAdditionalRecoOptions()

    def setAdditionalPreprocessOptions(self, options):
        assert isinstance(options, str)
        self._tabs._expertWidget.resetAdditionalPreprocessOptions()

    def loadFromScan(self, scanID):
        self._tabs.loadFromScan(scanID)
        self._scanTypeChanged()


class _TofuTab(_TofuOptionLoader, qt.QTabWidget):
    __doc__ = '\n    Tab containing the different editor for the tofu reconstruction parameter\n    '

    def __init__(self, parent):
        qt.QTabWidget.__init__(self, parent)
        self._outputWidget = OutputTofuWidget(parent=self)
        icon = icons.getQIcon('output')
        self.addTab(self._outputWidget, icon, 'Output definition')
        self._inputWidget = InputProjectionsScrollArea(parent=self)
        icon = icons.getQIcon('input')
        self.addTab(self._inputWidget, icon, 'Projections')
        self._expertWidget = ExpertTofuWidget(parent=self)
        icon = icons.getQIcon('parameters')
        self.addTab(self._expertWidget, icon, 'Expert')
        _TofuOptionLoader.__init__(self, options=[], childs=[self._outputWidget,
         self._inputWidget,
         self._expertWidget])
        self._expertWidget._gpuGrp.gpuOptionChanged.connect(self.gpuOptionUpdated)

    def loadFromScan(self, scanID):
        for widget in (self._outputWidget, self._inputWidget,
         self._expertWidget):
            widget.loadFromScan(scanID=scanID)

    def getAdditionalRecoOptions(self):
        return self._expertWidget.getAdditionalRecoOptions()

    def getAdditionalPreprocessOptions(self):
        return self._expertWidget.getAdditionalPreprocessOptions()

    def gpuOptionUpdated(self):
        highLimit = self._expertWidget.getHighLimit()
        self._outputWidget.setHighLimit(highLimit)


class ScanTypeWidget(_TofuOptionLoader, qt.QWidget):
    __doc__ = '\n    Simple widget to define the type of reconstruction we want\n    '

    def __init__(self, parent):
        qt.QWidget.__init__(self, parent)
        _TofuOptionLoader.__init__(self, options={'scan_type': self.setScanType})
        self.setLayout(qt.QHBoxLayout())
        self.layout().addWidget(qt.QLabel('scan type:', parent=self))
        self._scanType = qt.QComboBox(parent=self)
        for _type in SCAN_TYPES:
            self._scanType.addItem(_type)

        self.layout().addWidget(self._scanType)

    def setScanType(self, scan_type):
        assert scan_type in SCAN_TYPES_I
        index = self._scanType.findText(SCAN_TYPES_I[scan_type])
        assert index >= 0
        self._scanType.setCurrentIndex(index)

    def getScanType(self):
        return SCAN_TYPES[self._scanType.currentText()]