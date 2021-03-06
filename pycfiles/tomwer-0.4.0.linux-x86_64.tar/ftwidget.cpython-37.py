# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/gui/reconstruction/ftserie/reconsparamseditor/ftwidget.py
# Compiled at: 2020-03-06 02:01:31
# Size of source mod 2**32: 15489 bytes
__author__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '10/01/2018'
from silx.gui import qt, icons as silxicons
from tomwer.core.log import TomwerLogger
from tomwer.core.process.reconstruction.ftseries.params.ft import FixedSliceMode, VolSelMode
from tomwer.gui.reconstruction.ftserie.h5editor import H5StructEditor
from tomwer.synctools.ftseries import QReconsParams, _QFTRP
from tomwer.gui.utils.inputwidget import SelectionLineEdit
from tomwer.gui.utils.lineselector import QLineSelectorDialog
from tomwer.core.scan.scanbase import TomoBase
from silx.io.utils import get_data
import silx.gui.dialog.ImageFileDialog as ImageFileDialog
logger = TomwerLogger(__name__)

class FTWidget(H5StructEditor, qt.QWidget):
    __doc__ = '\n    Definition of the Main tab to edit the FT parameters\n    \n    :param int rpid: id of the reconstruction parameters edited by the widget\n    '
    _ROW_N_INDEX = 1

    def __init__(self, reconsparams, parent=None):
        qt.QWidget.__init__(self, parent)
        H5StructEditor.__init__(self, structID='FT')
        self._recons_params = None
        self._FTWidget__scan = None
        self.setReconsParams(reconsparams)
        self.setLayout(qt.QVBoxLayout())
        self.layout().addWidget(self._FTWidget__buildReconsOneSlice())
        self.layout().addWidget(self._FTWidget__buildSelectSlice())
        self.layout().addWidget(self._FTWidget__buildVolFile())
        self.layout().addWidget(self._FTWidget__buildVolumeSelection())
        self.layout().addWidget(self._FTWidget__buildPreviousVolumeSelection())
        self._qcbVolumeSelection.currentIndexChanged.connect(self._updatePreviousSelection)
        self.layout().addWidget(self._FTWidget__buildSpikeThreshokd())
        self.layout().addWidget(self._FTWidget__buildRingCorrection())
        spacer = qt.QWidget(self)
        spacer.setSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Expanding)
        self.layout().addWidget(spacer)
        self._makeConnection()

    def setReconsParams(self, recons_params):
        if isinstance(recons_params, QReconsParams):
            _recons_params = recons_params.ft
        else:
            if isinstance(recons_params, _QFTRP):
                _recons_params = recons_params
            else:
                raise ValueError('recons_params should be an instance of QReconsParam or _QFTRP')
        if self._recons_params:
            self._recons_params.sigChanged.disconnect(self._update_params)
        self._recons_params = _recons_params
        self.load(self._recons_params)
        self._recons_params.sigChanged.connect(self._update_params)

    def setScan(self, scan):
        self._FTWidget__scan = scan

    def _update_params(self):
        """Update all parameter"""
        self.load(self._recons_params)

    def _makeConnection(self):
        self._qcbDoTestSlice.toggled.connect(self._reconsOneSliceChanged)
        self._qleSliceN.textChanged.connect(self._reconsSelectSliceChanged)
        self._qcbSelectSlice.currentIndexChanged.connect(self._reconsSelectSliceChanged)
        self._qcbEDFStack.toggled.connect(self._volFileChanged)
        self._qcbVolumeSelection.currentIndexChanged.connect(self._volSelectChanged)
        self._qcbVolSelRemenber.toggled.connect(self._volSelectRemenberChanged)
        self._grpThreshold.toggled.connect(self._spikethresholdChanged)
        self._qleThresholdSpikesRm.editingFinished.connect(self._spikethresholdChanged)
        self._qcbRingsCorrection.toggled.connect(self._ringsCorrectionChanged)
        self._onRadioButton.pressed.connect(self._onRadioActivated)

    def __buildReconsOneSlice(self):
        self._qcbDoTestSlice = qt.QCheckBox('Reconstruct slice(s)', parent=self)
        self.linkCheckboxWithH5Variable(self._qcbDoTestSlice, 'DO_TEST_SLICE')
        return self._qcbDoTestSlice

    def _reconsOneSliceChanged(self, b):
        if self._isLoading is False:
            self._recons_params._set_parameter_value(parameter='DO_TEST_SLICE', value=(int(b)))
            self._sliceSelectionWidget.setEnabled(b)

    def __buildSelectSlice(self):
        self._sliceSelectionWidget = qt.QWidget()
        self._sliceSelectionWidget.setLayout(qt.QHBoxLayout())
        self._sliceSelectionWidget.layout().addWidget(qt.QLabel('Select slices to be reconstructed'))
        self._qcbSelectSlice = qt.QComboBox(parent=(self._sliceSelectionWidget))
        self._qcbSelectSlice.addItem(FixedSliceMode.middle.name)
        self._qcbSelectSlice.insertItem(self._ROW_N_INDEX, FixedSliceMode.row_n.name.replace('_', ' '))
        self._qcbSelectSlice.currentIndexChanged.connect(self._setEditableSliceIndex)
        self._sliceSelectionWidget.layout().addWidget(self._qcbSelectSlice)
        self._qleSliceN = SelectionLineEdit(text='0', parent=(self._sliceSelectionWidget))
        self._sliceSelectionWidget.layout().addWidget(self._qleSliceN)
        self._qleSliceN.hide()
        self.linkGroupWithH5Variable(group=(self._qleSliceN), h5ParamName='FIXEDSLICE',
          setter=(self._setFixedSlice),
          getter=(self._getFixedSlice))
        self._sliceSelectionWidget.layout().addWidget(self._qleSliceN)
        onRadioIcon = silxicons.getQIcon('window-new')
        self._onRadioButton = qt.QPushButton(onRadioIcon, 'on radio', parent=self)
        self._onRadioButton.setToolTip('Open a dialog to pick the rows froma radio')
        self._sliceSelectionWidget.layout().addWidget(self._onRadioButton)
        self._onRadioButton.hide()
        self._sliceSelectionWidget.setEnabled(self._recons_params.do_test_slice)
        return self._sliceSelectionWidget

    def _reconsSelectSliceChanged(self, *args, **kwargs):
        if self._isLoading is False:
            old = self._recons_params.blockSignals(True)
            value = self._getFixedSlice()
            self._recons_params._set_parameter_value(parameter='FIXEDSLICE', value=value)
            self._recons_params.blockSignals(old)

    def _setFixedSlice(self, val):
        if val == FixedSliceMode.middle:
            self._qcbSelectSlice.setCurrentIndex(0)
        else:
            try:
                nbslice = str(val)
            except ValueError as e:
                try:
                    warning = 'Cannot set nb slice value, '
                    if len(e.args) > 0:
                        warning += e.args[0]
                    logger.warning(warning)
                finally:
                    e = None
                    del e

            else:
                self._qcbSelectSlice.setCurrentIndex(self._ROW_N_INDEX)
                self._qleSliceN.setText(str(nbslice))

    def _getFixedSlice(self):
        if self._qcbSelectSlice.currentIndex() == self._ROW_N_INDEX:
            return self._qleSliceN.text()
        return self._qcbSelectSlice.currentText()

    def _setEditableSliceIndex(self):
        is_row_n_active = self._qcbSelectSlice.currentIndex() == self._ROW_N_INDEX
        self._qleSliceN.setVisible(is_row_n_active)
        self._onRadioButton.setVisible(is_row_n_active)

    def __buildVolFile(self):
        group = qt.QGroupBox('Select output mode :', parent=self)
        group.setLayout(qt.QHBoxLayout())
        self._qcbEDFStack = qt.QRadioButton('Stack of edf files', parent=group)
        group.layout().addWidget(self._qcbEDFStack)
        self._qcbEDFStack.setChecked(True)
        self._qcbSingleVolFile = qt.QRadioButton('Single vol file', parent=group)
        group.layout().addWidget(self._qcbSingleVolFile)
        self.linkGroupWithH5Variable(group=group, h5ParamName='VOLOUTFILE',
          setter=(self._setSingleVolOrStack),
          getter=(self._getSingleVolOrStack))
        return group

    def _volFileChanged(self):
        if self._isLoading is False:
            value = self._getSingleVolOrStack()
            self._recons_params._set_parameter_value(parameter='VOLOUTFILE', value=value)

    def _onRadioActivated(self):
        lineSelection = QLineSelectorDialog(parent=self)
        if self._FTWidget__scan is None:
            logger.info('No scan defined, request user for defining the imageurl')
            dialog = ImageFileDialog()
            if dialog.exec_():
                data = dialog.selectedImage()
            else:
                return
        else:
            scan = self._FTWidget__scan
            assert isinstance(scan, TomoBase)
        try:
            projections = scan.getProjectionsUrl()
            index_radio = list(projections.keys())[(len(projections) // 2)]
            data = get_data(projections[index_radio])
        except Exception as e:
            try:
                logger.error('Fail to load radio data:', str(e))
                return
            finally:
                e = None
                del e

        lineSelection.setData(data)
        if self._recons_params.fixed_slice not in (0, '0'):
            lineSelection.setSelection(self._recons_params.fixed_slice)
        if lineSelection.exec_() == qt.QDialog.Accepted:
            self._recons_params.fixed_slice = lineSelection.getSelection()

    def __buildVolumeSelection(self):
        widget = qt.QWidget(self)
        widget.setLayout(qt.QVBoxLayout())
        widget.layout().addWidget(qt.QLabel('Volume selection :'))
        self._qcbVolumeSelection = qt.QComboBox(self)
        self._qcbVolumeSelection.addItem(VolSelMode.total.name)
        self._qcbVolumeSelection.addItem(VolSelMode.manual.name)
        self._qcbVolumeSelection.addItem(VolSelMode.graphics.name)
        self.linkComboboxWithH5Variable(self._qcbVolumeSelection, 'VOLSELECT')
        widget.layout().addWidget(self._qcbVolumeSelection)
        return widget

    def _volSelectChanged(self):
        if self._isLoading is False:
            value = self._qcbVolumeSelection.currentText()
            self._recons_params._set_parameter_value(parameter='VOLSELECT', value=value)

    def __buildPreviousVolumeSelection(self):
        self._qcbVolSelRemenber = qt.QCheckBox('Remember previous volume selection', parent=self)
        self.linkCheckboxWithH5Variable((self._qcbVolSelRemenber), h5ParamName='VOLSELECTION_REMEMBER')
        return self._qcbVolSelRemenber

    def _volSelectRemenberChanged(self, b):
        if self._isLoading is False:
            value = int(b)
            self._recons_params._set_parameter_value(parameter='VOLSELECTION_REMEMBER', value=value)

    def __buildSpikeThreshokd(self):
        self._grpThreshold = qt.QGroupBox(title='Correct spikes', parent=self)
        self._grpThreshold.setCheckable(True)
        self._grpThreshold.setChecked(True)
        self._grpThreshold.setLayout(qt.QHBoxLayout())
        self._grpThreshold.layout().addWidget(qt.QLabel('Threshold for spikes removal'))
        self._qleThresholdSpikesRm = qt.QLineEdit('', parent=(self._grpThreshold))
        self._grpThreshold.layout().addWidget(self._qleThresholdSpikesRm)
        self.linkGroupWithH5Variable(group=(self._grpThreshold), h5ParamName='CORRECT_SPIKES_THRESHOLD',
          setter=(self._setSpikeThreshold),
          getter=(self._getSpikeThreshold))
        return self._grpThreshold

    def _spikethresholdChanged(self):
        if self._isLoading is False:
            value = self._getSpikeThreshold()
            self._recons_params._set_parameter_value(parameter='CORRECT_SPIKES_THRESHOLD', value=value)

    def __buildRingCorrection(self):
        self._qcbRingsCorrection = qt.QCheckBox('Perform rings corrections in PyHST', parent=self)
        self.linkCheckboxWithH5Variable(self._qcbRingsCorrection, 'RINGSCORRECTION')
        return self._qcbRingsCorrection

    def _ringsCorrectionChanged(self, b):
        if self._isLoading is False:
            value = int(b)
            self._recons_params._set_parameter_value(parameter='RINGSCORRECTION', value=value)

    def _getSingleVolOrStack(self):
        """return:
            - 0 if we want to use a single file for volume
            - 1 if we want to use a stack of edf file for volume
        """
        return int(not self._qcbEDFStack.isChecked())

    def _setSingleVolOrStack(self, val):
        """Set the value of the volume file selection
        """
        if not isinstance(val, (int, float, bool)):
            raise AssertionError
        else:
            assert int(val) in (0, 1)
            if val == 0:
                self._qcbEDFStack.setChecked(True)
            else:
                self._qcbSingleVolFile.setChecked(True)

    def _enableVolumeSelection(self, disable):
        """Do we give the user access to the volume selection or is it set to
        total
        """
        self._qcbVolumeSelection.setEnabled(not disable)
        if not disable:
            self._qcbVolumeSelection.setCurrentIndex(0)

    def _updatePreviousSelection(self):
        self._qcbVolSelRemenber.setEnabled(self._qcbVolumeSelection.currentIndex() == 1)

    def _setSpikeThreshold(self, value):
        if type(value) is str:
            assert value.lower() == 'inf'
            self._grpThreshold.setChecked(False)
        else:
            assert type(value) is float
            self._grpThreshold.setChecked(True)
            self._qleThresholdSpikesRm.setText(str(value))

    def _getSpikeThreshold(self):
        if self._grpThreshold.isChecked():
            return float(self._qleThresholdSpikesRm.text())
        return 'Inf'