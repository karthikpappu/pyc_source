# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/gui/reconstruction/axis/radioaxis.py
# Compiled at: 2020-03-06 02:01:31
# Size of source mod 2**32: 58219 bytes
"""
contains gui relative to axis calculation using radios
"""
__authors__ = [
 'C. Nemoz', 'H. Payno']
__license__ = 'MIT'
__date__ = '25/02/2019'
from silx.gui import qt
from tomwer.core.log import TomwerLogger
from tomwer.core.utils import image
import functools, numpy, enum, os
from .CompareImages import MODE_RAW_COMPARISON
from tomwer.core.scan.scanbase import ScanBase
from tomwer.core.scan.scanfactory import ScanFactory
from tomwer.synctools.axis import QAxisRP
from tomwer.core.process.reconstruction.axis.mode import AxisMode
from tomwer.core.process.reconstruction.axis.anglemode import CorAngleMode
from tomwer.gui.UrlSelectionTable import ColumnMode, UrlSelectionDialog
from tomwer.core.process.reconstruction.axis.params import AxisCalculationInput
from tomwer.core.process.reconstruction.axis.projectiontype import ProjectionType
from collections import OrderedDict
import scipy.signal
from .CompareImages import CompareImages
from tomwer.gui.utils.buttons import PadlockButton
_logger = TomwerLogger(__name__)

class RadioAxisWindow(qt.QMainWindow):
    __doc__ = '\n    QMainWindow for defining the rotation axis\n\n    .. snapshotqt:: img/AxisWindow.png\n\n        from tomwer.gui.ftserie.axis import AxisWindow\n        from tomwer.synctools.ftseries import QReconsParams\n        import scipy.misc\n        import scipy.ndimage\n\n        recons_params = QReconsParams()\n        widget = AxisWindow(recons_params)\n        imgA = scipy.misc.ascent()\n        imgB = scipy.ndimage.affine_transform(imgA, (1, 1), offset=(0, 10))\n\n        widget.setImages(imgA=imgA, imgB=imgB, flipB=False)\n        widget.show()\n\n    :raises ValueError: given axis is not an instance of _QAxisRP\n    '
    sigComputationRequested = qt.Signal()
    sigApply = qt.Signal()
    sigAxisEditionLocked = qt.Signal(bool)

    def __init__(self, axis, parent=None):
        qt.QMainWindow.__init__(self, parent)
        if isinstance(axis, QAxisRP):
            self._RadioAxisWindow__recons_params = axis
        else:
            raise TypeError('axis should be an instance of _QAxisRP')
        self._imgA = None
        self._imgB = None
        self._shiftedImgA = None
        self._flipB = True
        self._RadioAxisWindow__callback = None
        self._scan = None
        self._axis_params = None
        self._lastManualFlip = None
        self.setWindowFlags(qt.Qt.Widget)
        self._mainWidget = CompareImages(parent=self)
        _mode = MODE_RAW_COMPARISON
        self._mainWidget.setVisualizationMode(_mode)
        self.setCentralWidget(self._mainWidget)
        self._dockWidgetCtrl = qt.QDockWidget(parent=self)
        self._dockWidgetCtrl.layout().setContentsMargins(0, 0, 0, 0)
        self._dockWidgetCtrl.setFeatures(qt.QDockWidget.DockWidgetMovable)
        self._controlWidget = _AxisManual(parent=self, reconsParams=(self._RadioAxisWindow__recons_params))
        self._dockWidgetCtrl.setWidget(self._controlWidget)
        self.addDockWidget(qt.Qt.RightDockWidgetArea, self._dockWidgetCtrl)
        self._buttons = qt.QWidget(parent=self)
        self._buttons.setLayout(qt.QHBoxLayout())
        self._lockBut = PadlockButton(parent=self)
        self._buttons.layout().addWidget(self._lockBut)
        self._lockLabel = qt.QLabel('lock axis position', parent=self)
        self._buttons.layout().addWidget(self._lockLabel)
        spacer = qt.QWidget(self)
        spacer.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Minimum)
        self._buttons.layout().addWidget(spacer)
        self._computeBut = qt.QPushButton('compute', parent=self)
        self._buttons.layout().addWidget(self._computeBut)
        style = qt.QApplication.style()
        applyIcon = style.standardIcon(qt.QStyle.SP_DialogApplyButton)
        self._applyBut = qt.QPushButton(applyIcon, 'validate', parent=self)
        self._buttons.layout().addWidget(self._applyBut)
        self._controlWidget.layout().addWidget(self._buttons)
        self.getXShift = self._controlWidget.getXShift
        self.getYShift = self._controlWidget.getYShift
        self._setShift = self._controlWidget.setShift
        self.setXShift = self._controlWidget.setXShift
        self.setYShift = self._controlWidget.setYShift
        self.getShiftStep = self._controlWidget.getShiftStep
        self.setShiftStep = self._controlWidget.setShiftStep
        self.getAxis = self._controlWidget.getAxis
        self.getMode = self._controlWidget.getMode
        self.isLocked = self._lockBut.isLocked
        self.setPosition = self._controlWidget._positionInfoWidget.setPosition
        self._controlWidget.sigShiftChanged.connect(self._updateShift)
        self._controlWidget.sigRoiChanged.connect(self._updateShift)
        self._controlWidget.sigAuto.connect(self._updateAuto)
        self._controlWidget.sigModeChanged.connect(self._modeChanged)
        self._lockBut.toggled.connect(self.setLocked)
        self._computeBut.pressed.connect(self._computationRequested)
        self._applyBut.pressed.connect(self._validated)
        self._RadioAxisWindow__recons_params.sigChanged.connect(self._reset_scan)
        self._mainWidget.flipToggled.connect(self._flipChanged)
        self.setReconsParams(axis=(self._RadioAxisWindow__recons_params))
        self._mainWidget.setRadio2FlipVisible(self.getMode() == AxisMode.manual)
        self._computeBut.setVisible(self.getMode() is not AxisMode.manual)

    def _modeChanged(self, mode):
        mode = AxisMode.from_value(mode)
        mode_is_manual = mode == AxisMode.manual
        self._mainWidget.setRadio2FlipVisible(mode_is_manual)
        if mode_is_manual:
            if self._lastManualFlip is None:
                self._lastManualFlip = self._mainWidget.isRadio2Flip()
            else:
                self._setRadio2Flip(self._lastManualFlip)
        else:
            self._setRadio2Flip(checked=True)
        self._computeBut.setVisible(self.getMode() is not AxisMode.manual)
        old_control = self._controlWidget.blockSignals(True)
        self._controlWidget.setMode(mode)
        self._controlWidget.blockSignals(old_control)

    def getROI(self):
        if self.getMode() == AxisMode.manual:
            return self._controlWidget.getROI()
        return

    def _computationRequested(self):
        self.sigComputationRequested.emit()

    def setLocked(self, locked):
        old = self.blockSignals(True)
        if self._axis_params.mode not in (AxisMode.read, AxisMode.manual):
            self._axis_params.mode = AxisMode.manual
        self._controlWidget.setLocked(locked)
        self._lockBut.setChecked(locked)
        self.blockSignals(old)
        self.sigAxisEditionLocked.emit(locked)

    def _validated(self):
        """callback when the validate button is activated"""
        self.sigApply.emit()

    def _setRadio2Flip(self, checked):
        self._mainWidget.setRadio2Flip(checked)

    def _flipChanged(self, checked):
        if self.getMode() == AxisMode.manual:
            self._lastManualFlip = self._mainWidget.isRadio2Flip()
        if checked == self._flipB:
            return
        self._flipB = checked
        self._updatePlot()

    def setReconsParams(self, axis):
        """

        :param AxisRP axis: axis to edit
        :return: 
        """
        assert isinstance(axis, QAxisRP)
        self._axis_params = axis
        old = self.blockSignals(True)
        self.resetShift()
        self._controlWidget.setAxis(axis)
        self.blockSignals(old)

    def setScan(self, scan):
        """
        Update the interface concerning the given scan. Try to display the
        radios for angle 0 and 180.

        :param scan: scan for which we want the axis updated.
        :type scan: Union[str, tomwer.core.scan.TomoBase]
        """
        self.clear()
        _scan = scan
        if type(scan) is str:
            try:
                _scan = ScanFactory.create_scan_object(scan)
            except ValueError:
                raise ValueError('Fail to discover a valid scan in %s' % scan)

        else:
            if not isinstance(_scan, ScanBase):
                raise ValueError('type of %s (%s) is invalid, scan should be a file/dir path or an instance of ScanBase' % (
                 scan, type(scan)))
        assert isinstance(_scan, ScanBase)
        if _scan.axis_params is None:
            _scan.axis_params = QAxisRP()
        if self._scan is not None:
            self._scan.axis_params.sigAxisUrlChanged.disconnect(self._updatePlot)
        self._scan = _scan
        self._scan.axis_params.sigAxisUrlChanged.connect(self._updatePlot)
        self._updatePlot()
        self._controlWidget.setScan(scan=(self._scan))

    def _updatePlot(self):
        if self._scan is None:
            return
        else:
            coreAngleMode = CorAngleMode.from_value(self._RadioAxisWindow__recons_params.angle_mode)
            axis_rp = self._scan.axis_params
            if coreAngleMode is CorAngleMode.manual_selection:
                if axis_rp.n_url() == 2:
                    pass
                else:
                    res = self._scan.getRadiosForAxisCalc(mode=coreAngleMode)
                    axis_rp.axis_url_1 = res[0]
                    axis_rp.axis_url_2 = res[1]
                if axis_rp.n_url() < 2:
                    _logger.error('Fail to detect radio for axis calculation')
            elif axis_rp.axis_url_1.url:
                log_ = self._RadioAxisWindow__recons_params.projection_type is ProjectionType.transmission
                axis_rp.axis_url_1.normalize_data((self._scan), log_=log_)
                axis_rp.axis_url_2.normalize_data((self._scan), log_=log_)
                paganin = self._RadioAxisWindow__recons_params.paganin_preproc
                if paganin:
                    imgA = axis_rp.axis_url_1.normalized_data_paganin
                    imgB = axis_rp.axis_url_2.normalized_data_paganin
                else:
                    imgA = axis_rp.axis_url_1.normalized_data
                    imgB = axis_rp.axis_url_2.normalized_data
                assert imgA is not None
                assert imgB is not None
                self.setImages(imgA=imgA, imgB=imgB)
            else:
                _logger.error('fail to find radios for angle 0 and 180. Unable to update axis gui')

    def clear(self):
        self._scan = None

    def _reset_scan(self):
        if self._scan:
            self.setScan(scan=(self._scan))

    def _showImgBBeFlipped(self):
        return self._mainWidget.getCompareToolBar().isRadio2Flip()

    def setImages(self, imgA, imgB):
        """

        :warning: does not reset the shift when change images

        :param numpy.array imgA: first image to compare. Will be the one shifted
        :param numpy.array imgB: second image to compare
        :param bool flipB: True if the image B has to be flipped
        :param bool paganin: True to apply paganin phase retrieval
        """
        flipB = self._showImgBBeFlipped()
        if not imgA is not None:
            raise AssertionError
        elif not imgB is not None:
            raise AssertionError
        else:
            _imgA = imgA
            _imgB = imgB
            if _imgA.shape != _imgB.shape:
                _logger.error('The two provided images have incoherent shapes (%s vs %s)' % (
                 _imgA.shape, _imgB.shape))
            else:
                if _imgA.ndim is not 2:
                    _logger.error('Image shape are not 2 dimensional')
                else:
                    self._flipB = flipB
                    self._imgA = _imgA
                    self._imgB = _imgB
                    self._controlWidget._roiControl.setLimits(width=(self._imgA.shape[1]), height=(self._imgA.shape[0]))
                    self._updateShift(xShift=(self.getXShift()), yShift=(self.getYShift()))

    def _updateShift(self, xShift=None, yShift=None):
        self._controlWidget._positionInfoWidget._updatePosition()
        if self._imgA is None or self._imgB is None:
            return
        xShift = xShift or self.getXShift()
        yShift = yShift or self.getYShift()
        _imgA, _imgB = self._getRawImages()
        if xShift == 0.0 and yShift == 0.0:
            self._shiftedImgA = _imgA
        else:
            try:
                self._shiftedImgA = image.shift_img(data=_imgA, dx=(self.getXShift()),
                  dy=(self.getYShift()))
            except ValueError as e:
                try:
                    _logger.warning(e)
                finally:
                    e = None
                    del e

            self._mainWidget.setData(image1=(self._shiftedImgA), image2=_imgB)

    def _getRawImages(self):

        def selectROI(data, width, height):
            x_center = data.shape[1] // 2
            y_center = data.shape[0] // 2
            x_min = x_center - width // 2
            x_max = x_center + width // 2
            y_min = y_center - height // 2
            y_max = y_center + height // 2
            return data[y_min:y_max, x_min:x_max]

        _roi = self.getROI()
        _imgA = self._imgA
        _imgB = self._imgB
        if self._flipB is True:
            _imgB = numpy.fliplr(_imgB)
        if _roi is not None:
            assert type(_roi) is tuple
            _imgA = selectROI(_imgA, width=(_roi[0]), height=(_roi[1]))
            _imgB = selectROI(_imgB, width=(_roi[0]), height=(_roi[1]))
        return (
         _imgA, _imgB)

    def _updateAuto(self):
        _imgA, _imgB = self._getRawImages()
        correlation = scipy.signal.correlate2d(in1=_imgA, in2=_imgB)
        y, x = numpy.unravel_index(numpy.argmax(correlation), correlation.shape)
        self._setShift(x=x, y=y)

    def resetShift(self):
        self._controlWidget.blockSignals(True)
        self._controlWidget.reset()
        self._controlWidget.blockSignals(False)
        if self._imgA:
            if self._imgB:
                self.setImages(imgA=(self._imgA), imgB=(self._imgB))


class _AxisRead(qt.QWidget):
    __doc__ = 'Widget to select a position value from a file'
    sigFileChanged = qt.Signal(str)

    def __init__(self, parent, axis=None):
        qt.QWidget.__init__(self, parent)
        self._axis = None
        if axis:
            self.setAxis(axis)
        self.setLayout(qt.QHBoxLayout())
        self.layout().addWidget(qt.QLabel('File', parent=self))
        self._filePathQLE = qt.QLineEdit('', parent=self)
        self.layout().addWidget(self._filePathQLE)
        self._fileSelPB = qt.QPushButton('select', parent=self)
        self.layout().addWidget(self._fileSelPB)
        self._fileSelPB.pressed.connect(self._selectFile)
        self._filePathQLE.textChanged.connect(self._fileChanged)

    def setAxis(self, axis):
        assert isinstance(axis, QAxisRP)
        self._axis = axis

    def _selectFile(self):
        dialog = qt.QFileDialog(self)
        dialog.setFileMode(qt.QFileDialog.ExistingFile)
        if not dialog.exec_():
            dialog.close()
            return
        _file_path = dialog.selectedFiles()[0]
        _logger.info('user select file %s for reading position value' % _file_path)
        self._filePathQLE.setText(dialog.selectedFiles()[0])

    def _fileChanged(self, file_path):
        """callback when the line edit (containing the file path) changed"""
        if self._axis:
            if os.path.isfile(file_path):
                self._axis.set_position_frm_par_file(file_path, force=True)


class _PositionInfoWidget(qt.QWidget):
    __doc__ = 'Widget used to display information relative to the current position'

    def __init__(self, parent, axis=None):
        self._axis = None
        qt.QWidget.__init__(self, parent)
        self.setLayout(qt.QHBoxLayout())
        centerLabel = qt.QLabel('center:', parent=self)
        centerLabel.setSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
        font = centerLabel.font()
        font.setBold(True)
        centerLabel.setFont(font)
        self.layout().addWidget(centerLabel)
        self._positionLabel = qt.QLabel('', parent=self)
        self._positionLabel.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Minimum)
        palette = self._positionLabel.palette()
        palette.setColor(qt.QPalette.WindowText, qt.QColor(qt.Qt.red))
        self._positionLabel.setPalette(palette)
        self._positionLabel.setAlignment(qt.Qt.AlignLeft)
        self.layout().addWidget(self._positionLabel)
        if axis:
            self.setAxis(axis)

    def setAxis(self, axis):
        assert isinstance(axis, QAxisRP)
        if axis == self._axis:
            return
        if self._axis is not None:
            self._axis.sigChanged.disconnect(self._updatePosition)
        self._axis = axis
        self._axis.sigChanged.connect(self._updatePosition)
        self._updatePosition()

    def _updatePosition(self):
        if self._axis:
            if self._axis.value is None:
                value = '?'
            else:
                value = str(self._axis.value)
            self._positionLabel.setText(value)

    def getPosition(self):
        return float(self._positionLabel.text())

    def setPosition(self, value):
        self._positionLabel.setText(str(value))


class _AxisManual(qt.QWidget):
    __doc__ = '\n    Widget to define the shift to apply on an image\n    '
    sigShiftChanged = qt.Signal(float, float)

    def __init__(self, parent, reconsParams):
        assert isinstance(reconsParams, QAxisRP)
        qt.QWidget.__init__(self, parent)
        self._xShift = 0
        self._yShift = 0
        self._recons_params = reconsParams or QAxisRP()
        self._axis = None
        self.setLayout(qt.QVBoxLayout())
        self._manualSelectionWidget = _AxisManualSelection(parent=self, shift_mode=(ShiftMode.x_only))
        self._manualSelectionWidget.layout().setContentsMargins(0, 0, 0, 0)
        self._readFileSelWidget = _AxisRead(parent=self)
        self._readFileSelWidget.layout().setContentsMargins(0, 0, 0, 0)
        self._displacementSelector = self._manualSelectionWidget._displacementSelector
        self._shiftControl = self._manualSelectionWidget._shiftControl
        self._roiControl = self._manualSelectionWidget._roiControl
        self._mainWidget = AxisTabWidget(parent=self, mode_dependant_widget=(self._manualSelectionWidget),
          read_file_sel_widget=(self._readFileSelWidget),
          recons_params=(self._recons_params))
        self.layout().addWidget(self._mainWidget)
        self._positionInfoWidget = _PositionInfoWidget(parent=self)
        self.layout().addWidget(self._positionInfoWidget)
        self._positionInfoWidget.layout().setContentsMargins(0, 0, 0, 0)
        callback = functools.partial(self._incrementShift, 'left')
        self._shiftControl.sigShiftLeft.connect(callback)
        callback = functools.partial(self._incrementShift, 'right')
        self._shiftControl.sigShiftRight.connect(callback)
        callback = functools.partial(self._incrementShift, 'top')
        self._shiftControl.sigShiftTop.connect(callback)
        callback = functools.partial(self._incrementShift, 'bottom')
        self._shiftControl.sigShiftBottom.connect(callback)
        self._shiftControl.sigReset.connect(self._resetShift)
        self._shiftControl.sigShiftChanged.connect(self._setShiftAndSignal)
        self.getShiftStep = self._displacementSelector.getShiftStep
        self.setShiftStep = self._displacementSelector.setShiftStep
        self.sigRoiChanged = self._roiControl.sigRoiChanged
        self.sigAuto = self._shiftControl.sigAuto
        self.getROI = self._roiControl.getROI
        self.getMode = self._mainWidget.getMode
        self.setScan = self._mainWidget.setScan
        self.sigModeChanged = self._mainWidget.sigModeChanged
        self.setAxis(self._recons_params)

    def _setShiftAndSignal(self, x, y):
        self.setShift(x, y)
        self._shiftControl._updateShiftInfo(x=x, y=y)
        self.sigShiftChanged.emit(x, y)

    def setAxis(self, axis):
        assert isinstance(axis, QAxisRP)
        old = self.blockSignals(True)
        if self._axis:
            self._axis.sigChanged.disconnect(self._updateAxisView)
        self._axis = axis
        self.setXShift(self._axis.value)
        self._mainWidget.setAxisParams(self._axis)
        self._readFileSelWidget.setAxis(self._axis)
        self._positionInfoWidget.setAxis(self._axis)
        self._updateAxisView()
        self._axis.sigChanged.connect(self._updateAxisView)
        self.blockSignals(old)

    def setMode(self, mode):
        self._axis.mode = mode
        self._updateAxisView()

    def _updateAxisView(self):
        self._axis.blockSignals(True)
        if self._axis.value not in (None, '...'):
            self.setXShift(self._axis.value)
            self._positionInfoWidget._updatePosition()
        self._axis.blockSignals(False)
        self._manualSelectionWidget.setVisible(self._axis.mode is AxisMode.manual)
        self._readFileSelWidget.setVisible(self._axis.mode is AxisMode.read)

    def getAxis(self):
        return self._axis

    def _incrementShift(self, direction):
        if not direction in ('left', 'right', 'top', 'bottom'):
            raise AssertionError
        elif direction == 'left':
            self.setXShift(self._xShift - self.getShiftStep())
        else:
            if direction == 'right':
                self.setXShift(self._xShift + self.getShiftStep())
            else:
                if direction == 'top':
                    self.setYShift(self._yShift + self.getShiftStep())
                else:
                    self.setYShift(self._yShift - self.getShiftStep())
        self._shiftControl._updateShiftInfo(x=(self._xShift), y=(self._yShift))
        self.sigShiftChanged.emit(self._xShift, self._yShift)

    def _resetShift(self):
        old = self._axis.blockSignals(True)
        self.setXShift(0)
        self.setYShift(0)
        self._shiftControl._updateShiftInfo(x=(self._xShift), y=(self._yShift))
        self._axis.blockSignals(old)
        self.sigShiftChanged.emit(self._xShift, self._yShift)

    def getXShift(self):
        if self._xShift == '...':
            return 0
        return self._xShift

    def getYShift(self):
        if self._yShift == '...':
            return 0
        return self._yShift

    def setXShift(self, x: float):
        self.setShift(x=x, y=(self._yShift))

    def setYShift(self, y):
        self.setShift(x=(self._xShift), y=y)

    def setShift(self, x, y):
        if x == self._xShift:
            if y == self._yShift:
                return
        self._xShift = x if x is not None else 0.0
        self._yShift = y if y is not None else 0.0
        if self._axis:
            old = self._axis.blockSignals(True)
            self._axis.value = x
            self._axis.blockSignals(old)
        self._shiftControl._updateShiftInfo(x=(self._xShift), y=(self._yShift))
        self.sigShiftChanged.emit(self._xShift, self._yShift)

    def reset(self):
        self._xShift = 0
        self._yShift = 0
        self.sigShiftChanged.emit(self._xShift, self._yShift)

    def setLocked(self, locked):
        self._mainWidget.setEnabled(not locked)


class _AxisManualSelection(qt.QWidget):

    def __init__(self, parent, shift_mode):
        qt.QWidget.__init__(self, parent)
        self.setLayout(qt.QVBoxLayout())
        self._displacementSelector = _DisplacementSelector(parent=self)
        self.layout().addWidget(self._displacementSelector)
        self._shiftControl = _ShiftControl(parent=self, shift_mode=shift_mode)
        self.layout().addWidget(self._shiftControl)
        self._roiControl = _ROIControl(parent=self)
        self.layout().addWidget(self._roiControl)


class _ROIControl(qt.QGroupBox):
    __doc__ = '\n    Widget used to define the ROI on images to compare\n    '
    sigRoiChanged = qt.Signal(object)

    def __init__(self, parent):
        qt.QGroupBox.__init__(self, 'ROI selection', parent)
        self.setLayout(qt.QVBoxLayout())
        self._buttonGrp = qt.QButtonGroup(parent=self)
        self._buttonGrp.setExclusive(True)
        self._roiWidget = qt.QWidget(parent=self)
        self._roiWidget.setLayout(qt.QHBoxLayout())
        self._roiWidget.layout().setContentsMargins(0, 0, 0, 0)
        self._roiButton = qt.QRadioButton('ROI', parent=(self._roiWidget))
        self._roiWidget.layout().addWidget(self._roiButton)
        self._buttonGrp.addButton(self._roiButton)
        self._roiDefinition = _ROIDefinition(parent=self)
        self._roiWidget.layout().addWidget(self._roiDefinition)
        self.layout().addWidget(self._roiWidget)
        self._fullImgButton = qt.QRadioButton('full image', parent=self)
        self._buttonGrp.addButton(self._fullImgButton)
        self.layout().addWidget(self._fullImgButton)
        self._roiButton.toggled.connect(self._roiDefinition.setEnabled)
        self.sigRoiChanged = self._roiDefinition.sigRoiChanged
        self.getROI = self._roiDefinition.getROI
        self.setLimits = self._roiDefinition.setLimits
        self._roiButton.setChecked(True)


class _ROIDefinition(qt.QWidget):
    __doc__ = '\n    Widget used to define ROI width and height.\n\n    :note: emit ROI == None if setDisabled\n    '
    sigRoiChanged = qt.Signal(object)

    def __init__(self, parent):
        qt.QWidget.__init__(self, parent)
        self.setLayout(qt.QGridLayout())
        self.layout().addWidget(qt.QLabel('width', parent=self), 0, 0)
        self._widthSB = qt.QSpinBox(parent=self)
        self._widthSB.setSingleStep(2)
        self._widthSB.setMaximum(10000)
        self._widthSB.setSuffix(' px')
        self.layout().addWidget(self._widthSB, 0, 1)
        self.layout().addWidget(qt.QLabel('height', parent=self), 1, 0)
        self._heightSB = qt.QSpinBox(parent=self)
        self._heightSB.setSingleStep(2)
        self._heightSB.setSuffix(' px')
        self._heightSB.setMaximum(10000)
        self.layout().addWidget(self._heightSB, 1, 1)
        self._widthSB.editingFinished.connect(self._ROIDefinition__roiChanged)
        self._heightSB.editingFinished.connect(self._ROIDefinition__roiChanged)

    def __roiChanged(self, *args, **kwargs):
        self.sigRoiChanged.emit(self.getROI())

    def setLimits(self, width, height):
        """

        :param int x: width maximum value
        :param int height: height maximum value
        """
        for spinButton in (self._widthSB, self._heightSB):
            spinButton.blockSignals(True)

        assert type(width) is int
        assert type(height) is int
        valueChanged = False
        if self._widthSB.value() > width:
            self._widthSB.setValue(width)
            valueChanged = True
        if self._heightSB.value() > height:
            self._heightSB.setValue(height)
            valueChanged = True
        if self._widthSB.value() is 0:
            self._widthSB.setValue(min(256, width))
            valueChanged = True
        if self._heightSB.value() is 0:
            self._heightSB.setValue(min(256, height))
            valueChanged = True
        self._widthSB.setRange(1, width)
        self._heightSB.setRange(1, height)
        for spinButton in (self._widthSB, self._heightSB):
            spinButton.blockSignals(False)

        if valueChanged is True:
            self._ROIDefinition__roiChanged()

    def getROI(self):
        """

        :return: (width, height) or None
        :rtype: Union[None, tuple]
        """
        if self.isEnabled():
            return (
             self._widthSB.value(), self._heightSB.value())
        return

    def setEnabled(self, *arg, **kwargs):
        (qt.QWidget.setEnabled)(self, *arg, **kwargs)
        self._ROIDefinition__roiChanged()


@enum.unique
class ShiftMode(enum.Enum):
    x_only = 0
    y_only = 1
    x_and_y = 2


class _ShiftControl(qt.QWidget):
    __doc__ = '\n    Widget to control the shift step we want to apply\n    '
    sigShiftLeft = qt.Signal()
    sigShiftRight = qt.Signal()
    sigShiftTop = qt.Signal()
    sigShiftBottom = qt.Signal()
    sigReset = qt.Signal()
    sigAuto = qt.Signal()
    sigShiftChanged = qt.Signal(float, float)

    def __init__(self, parent, shift_mode):
        """

        :param parent: qt.QWidget
        :param ShiftMode shift_mode: what are the shift we want to control
        """
        qt.QWidget.__init__(self, parent)
        self.setLayout(qt.QGridLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self._leftButton = qt.QPushButton('left', parent=self)
        self.layout().addWidget(self._leftButton, 1, 0)
        self._rightButton = qt.QPushButton('right', parent=self)
        self.layout().addWidget(self._rightButton, 1, 3)
        self._topButton = qt.QPushButton('top', parent=self)
        self.layout().addWidget(self._topButton, 0, 1)
        self._bottomButton = qt.QPushButton('bottom', parent=self)
        self.layout().addWidget(self._bottomButton, 2, 1)
        self._resetButton = qt.QPushButton('reset', parent=self)
        self.layout().addWidget(self._resetButton, 3, 2, 3, 4)
        self._autoButton = qt.QPushButton('auto', parent=self)
        self.layout().addWidget(self._autoButton, 3, 0, 3, 2)
        self._autoButton.hide()
        self._shiftInfo = _ShiftInformation(parent=self)
        self.layout().addWidget(self._shiftInfo, 1, 1)
        self._shiftInfo._updateShiftInfo(x=0.0, y=0.0)
        self._leftButton.pressed.connect(self.sigShiftLeft.emit)
        self._rightButton.pressed.connect(self.sigShiftRight.emit)
        self._topButton.pressed.connect(self.sigShiftTop.emit)
        self._bottomButton.pressed.connect(self.sigShiftBottom.emit)
        self._resetButton.pressed.connect(self.sigReset.emit)
        self._autoButton.pressed.connect(self.sigAuto.emit)
        self._shiftInfo.sigShiftChanged.connect(self.sigShiftChanged.emit)
        self._updateShiftInfo = self._shiftInfo._updateShiftInfo
        self.setShiftMode(shift_mode)

    def setShiftMode(self, shift_mode):
        show_x_shift = shift_mode in (ShiftMode.x_only, ShiftMode.x_and_y)
        show_y_shift = shift_mode in (ShiftMode.y_only, ShiftMode.x_and_y)
        self._leftButton.setVisible(show_x_shift)
        self._rightButton.setVisible(show_x_shift)
        self._topButton.setVisible(show_y_shift)
        self._bottomButton.setVisible(show_y_shift)
        self._shiftInfo._xLE.setVisible(show_x_shift)
        self._shiftInfo._xLabel.setVisible(show_x_shift)
        self._shiftInfo._yLE.setVisible(show_y_shift)
        self._shiftInfo._yLabel.setVisible(show_y_shift)


class _ShiftInformation(qt.QWidget):
    __doc__ = '\n    Widget displaying information about the current x and y shift.\n    Both x shift and y shift are editable.\n    '

    class _ShiftLineEdit(qt.QLineEdit):

        def __init__(self, *args, **kwargs):
            (qt.QLineEdit.__init__)(self, *args, **kwargs)
            validator = qt.QDoubleValidator(parent=self, decimals=2)
            self.setValidator(validator)

        def sizeHint(self):
            return qt.QSize(40, 10)

    sigShiftChanged = qt.Signal(float, float)

    def __init__(self, parent):
        qt.QWidget.__init__(self, parent)
        self.setLayout(qt.QHBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)
        self._xLabel = qt.QLabel('x=', parent=self)
        self.layout().addWidget(self._xLabel)
        self._xLE = _ShiftInformation._ShiftLineEdit('', parent=self)
        self.layout().addWidget(self._xLE)
        self._yLabel = qt.QLabel('y=', parent=self)
        self.layout().addWidget(self._yLabel)
        self._yLE = _ShiftInformation._ShiftLineEdit('', parent=self)
        self.layout().addWidget(self._yLE)
        self._xLE.editingFinished.connect(self._shiftChanged)
        self._yLE.editingFinished.connect(self._shiftChanged)

    def _updateShiftInfo(self, x, y):
        self.blockSignals(True)
        if x is None:
            x = 0.0
        if y is None:
            y = 0.0
        x_text = x
        if x_text != '...':
            x_text = '%.1f' % float(x)
        y_text = y
        if y_text != '...':
            y_text = '%.1f' % float(y)
        self._xLE.setText(x_text)
        self._yLE.setText(y_text)
        self.blockSignals(False)

    def _shiftChanged(self, *args, **kwargs):
        self.sigShiftChanged.emit(float(self._xLE.text()), float(self._yLE.text()))


class _DisplacementSelector(qt.QGroupBox):
    __doc__ = '\n    Group box to define the displacement step value\n    '

    def __init__(self, parent):
        qt.QGroupBox.__init__(self, 'shift step', parent)
        self.setLayout(qt.QVBoxLayout())
        self._buttonGrp = qt.QButtonGroup(parent=self)
        self._buttonGrp.setExclusive(True)
        self._rawButton = qt.QRadioButton('Raw (1 pixel)', parent=self)
        self.layout().addWidget(self._rawButton)
        self._buttonGrp.addButton(self._rawButton)
        self._fineButton = qt.QRadioButton('Fine (0.1 pixel)', parent=self)
        self.layout().addWidget(self._fineButton)
        self._buttonGrp.addButton(self._fineButton)
        self._manualWidget = qt.QWidget(parent=self)
        self._manualWidget.setLayout(qt.QHBoxLayout())
        self._manualWidget.layout().setContentsMargins(0, 0, 0, 0)
        self._manualWidget.layout().setSpacing(0)
        self._manualButton = qt.QRadioButton('Manual', parent=(self._manualWidget))
        self._manualWidget.layout().addWidget(self._manualButton)
        self._manualLE = qt.QLineEdit('0.5', parent=(self._manualWidget))
        validator = qt.QDoubleValidator(parent=(self._manualLE), decimals=2)
        validator.setBottom(0.0)
        self._manualLE.setValidator(validator)
        self._manualWidget.layout().addWidget(self._manualLE)
        self.layout().addWidget(self._manualWidget)
        self._manualLE.setEnabled(False)
        self._buttonGrp.addButton(self._manualButton)
        self._rawButton.setChecked(True)
        self._manualButton.toggled.connect(self._manualLE.setEnabled)

    def getShiftStep(self):
        """

        :return: displacement shift defined
        :rtype: float
        """
        if self._rawButton.isChecked():
            return 1.0
        if self._fineButton.isChecked():
            return 0.1
        return float(self._manualLE.text())

    def setShiftStep(self, value):
        """

        :param float value: shift step
        """
        assert type(value) is float
        self._manualButton.setChecked(True)
        self._manualLE.setText(str(value))


class _AxisOptionsWidget(qt.QWidget):
    __doc__ = 'GUI to tune the axis algorithm'

    def __init__(self, parent, axis):
        qt.QWidget.__init__(self, parent=parent)
        assert isinstance(axis, QAxisRP)
        self._axis = axis
        self.setLayout(qt.QVBoxLayout())
        self._commonOpts = qt.QWidget(parent=self)
        self._commonOpts.setLayout(qt.QFormLayout())
        self._qcbDataMode = qt.QComboBox(parent=self)
        for data_mode in AxisCalculationInput:
            self._qcbDataMode.addItem(data_mode.name(), data_mode)

        self._commonOpts.layout().addRow('data mode', self._qcbDataMode)
        self._scaleOpt = qt.QCheckBox(parent=self)
        self._commonOpts.layout().addRow('scale the two images', self._scaleOpt)
        self.layout().addWidget(self._commonOpts)
        self._nearOpts = _AxisNearOptsWidget(parent=self, axis=(self._axis))
        self.layout().addWidget(self._nearOpts)
        self.setCalculationInputType(self._axis.calculation_input_type)
        self._scaleOpt.toggled.connect(self._updateScaleOpt)
        self._qcbDataMode.currentIndexChanged.connect(self._updateInputType)
        self._axis.sigChanged.connect(self._updateMode)

    def setMode(self, mode):
        mode_ = AxisMode.from_value(mode)
        self._nearOpts.setVisible(mode_ == AxisMode.near)

    def _updateMode(self):
        old = self.blockSignals(True)
        self._nearOpts.setVisible(self._axis.mode == AxisMode.near)
        index = self._qcbDataMode.findText(self._axis.calculation_input_type.name())
        if index >= 0:
            self._qcbDataMode.setCurrentIndex(index)
        self.blockSignals(old)

    def _updateScaleOpt(self, *arg, **kwargs):
        old = self._axis.blockSignals(True)
        self._axis.scale_img2_to_img1 = self.isImageScaled()
        self._axis.blockSignals(old)

    def isImageScaled(self):
        return self._scaleOpt.isChecked()

    def _updateInputType(self, *arg, **kwargs):
        self._axis.calculation_input_type = self.getCalulationInputType()

    def getCalulationInputType(self, *arg, **kwargs):
        return AxisCalculationInput.from_value(self._qcbDataMode.currentText())

    def setCalculationInputType(self, calculation_type):
        calculation_type = AxisCalculationInput.from_value(calculation_type)
        index_dm = self._qcbDataMode.findText(calculation_type.name())
        self._qcbDataMode.setCurrentIndex(index_dm)

    def setAxisParams(self, axis):
        self._nearOpts.setAxisParams(axis=axis)
        self._axis = axis
        old = self.blockSignals(True)
        self._scaleOpt.setChecked(axis.scale_img2_to_img1)
        index = self._qcbDataMode.findText(axis.calculation_input_type.name())
        self._qcbDataMode.setCurrentIndex(index)
        self.blockSignals(old)


class _AxisNearOptsWidget(qt.QWidget):
    __doc__ = 'GUI dedicated to the neat option'

    def __init__(self, parent, axis):
        qt.QWidget.__init__(self, parent=parent)
        assert isinstance(axis, QAxisRP)
        self._axis = axis
        self.setLayout(qt.QFormLayout())
        self._stdMaxOpt = qt.QCheckBox(parent=self)
        self.layout().addRow('look at max standard deviation', self._stdMaxOpt)
        self._nearWX = qt.QSpinBox(parent=self)
        self._nearWX.setMinimum(1)
        self._nearWX.setValue(5)
        self.layout().addRow('window size', self._nearWX)
        self._fineStepX = qt.QDoubleSpinBox(parent=self)
        self._fineStepX.setMinimum(0.05)
        self._fineStepX.setSingleStep(0.05)
        self._fineStepX.setMaximum(1.0)
        self.layout().addRow('fine step x', self._fineStepX)
        self._stdMaxOpt.toggled.connect(self._lookforStxMaxChanged)
        self._nearWX.valueChanged.connect(self._windowSizeChanged)
        self._fineStepX.valueChanged.connect(self._fineStepXChanged)

    def _lookforStxMaxChanged(self, *args, **kwargs):
        self._axis.look_at_stdmax = self.isLookAtStdMax()

    def isLookAtStdMax(self):
        """

        :return: is the option for looking at max standard deviation is
                 activated
        :rtype: bool
        """
        return self._stdMaxOpt.isChecked()

    def _windowSizeChanged(self, *args, **kwargs):
        self._axis.near_wx = self.getWindowSize()

    def getWindowSize(self):
        """

        :return: window size for near search
        :rtype: int
        """
        return self._nearWX.value()

    def _fineStepXChanged(self, *args, **kwargs):
        self._axis.fine_step_x = self.getFineStepX()

    def getFineStepX(self):
        """

        :return: fine step x for near calculation
        :rtype: float
        """
        return self._fineStepX.value()

    def setAxisParams(self, axis):
        """

        :param axis: axis to edit
        :type: AxisRP
        """
        old = self.blockSignals(True)
        self._axis = axis
        self._stdMaxOpt.setChecked(axis.look_at_stdmax)
        self._nearWX.setValue(axis.near_wx)
        self._fineStepX.setValue(axis.fine_step_x)
        self.blockSignals(old)


class AxisTabWidget(qt.QTabWidget):
    __doc__ = '\n    TabWidget containing all the information to edit the AXIS parameters\n    '

    def __init__(self, recons_params, parent=None, mode_dependant_widget=None, read_file_sel_widget=None):
        """

        :param recons_params: reconstruction parameters edited by the widget
        :type: QAxisRP
        :param mode_dependant_widget: widget used for manual selection of the
                                      axis
        :type mode_dependant_widget: Union[None, `._AxisManualSelection`]
        :param read_file_sel_widget: widget used to select a par file containing
                                     the axis position
        :type read_file_sel_widget: Union[None, `._AxisRead`]
        """
        qt.QTabWidget.__init__(self, parent)
        assert recons_params is not None
        self._calculationWidget = _CalculationWidget(parent=self, axis_params=recons_params)
        self._optionsWidget = _AxisOptionsWidget(parent=self, axis=recons_params)
        self._inputWidget = _InputWidget(parent=self, axis_params=recons_params)
        if mode_dependant_widget:
            self._calculationWidget.layout().addWidget(mode_dependant_widget)
        if read_file_sel_widget:
            self._calculationWidget.layout().addWidget(read_file_sel_widget)
        for widget in (self._calculationWidget, self._optionsWidget):
            spacer = qt.QWidget(self)
            spacer.setSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Expanding)
            widget.layout().addWidget(spacer)

        self._optionsSA = qt.QScrollArea(parent=self)
        self._optionsSA.setWidget(self._optionsWidget)
        self.addTab(self._calculationWidget, 'calculation')
        self.addTab(self._optionsSA, 'options')
        self.addTab(self._inputWidget, 'input')
        self.setAxisParams(recons_params)
        self._optionsWidget.setMode(self.getMode())
        self.sigModeChanged = self._calculationWidget.sigModeChanged

    def getMode(self):
        """Return algorithm to use for axis calculation"""
        return self._calculationWidget.getMode()

    def setScan(self, scan):
        self._inputWidget.setUrls(scan=scan)
        if scan is not None:
            self._inputWidget.setScanRange(scan.get_scan_range())

    def setAxisParams(self, axis):
        old = self.blockSignals(True)
        self._calculationWidget.setAxisParams(axis)
        self._optionsWidget.setAxisParams(axis)
        self._inputWidget.setAxisParams(axis)
        self.blockSignals(old)


class _CalculationWidget(qt.QWidget):
    __doc__ = 'Main widget to select the algorithm to use for COR calculation'
    sigModeChanged = qt.Signal(str)

    def __init__(self, parent, axis_params):
        assert isinstance(axis_params, QAxisRP)
        qt.QWidget.__init__(self, parent)
        self._axis_params = None
        self.setLayout(qt.QVBoxLayout())
        self._modeWidget = qt.QWidget(parent=self)
        self._modeWidget.setLayout(qt.QHBoxLayout())
        self.layout().addWidget(self._modeWidget)
        self._CalculationWidget__rotAxisSelLabel = qt.QLabel('algorithm to compute cor')
        self._modeWidget.layout().addWidget(self._CalculationWidget__rotAxisSelLabel)
        self._qcbPosition = qt.QComboBox(self)
        self._qcbPosition.addItem(AxisMode.global_.value)
        self._qcbPosition.addItem(AxisMode.manual.value)
        self._qcbPosition.addItem(AxisMode.near.value)
        self._qcbPosition.addItem(AxisMode.read.value)
        self._modeWidget.layout().addWidget(self._qcbPosition)
        self._qleNearPosQLE = qt.QLineEdit('0', parent=self)
        self._modeWidget.layout().addWidget(self._qleNearPosQLE)
        validator = qt.QDoubleValidator(parent=self)
        self._qleNearPosQLE.setValidator(validator)
        self._qleNearPosQLE.hide()
        self._qcbPosition.currentIndexChanged.connect(self._modeChanged)
        self._qleNearPosQLE.editingFinished.connect(self._nearValueChanged)
        self.setAxisParams(axis_params)

    def _modeChanged(self, *args, **kwargs):
        self._qleNearPosQLE.setVisible(self.getMode() == AxisMode.near)
        self.sigModeChanged.emit(self.getMode().value)

    def getMode(self):
        """Return algorithm to use for axis calculation"""
        return AxisMode.from_value(self._qcbPosition.currentText())

    def _nearValueChanged(self, *args, **kwargs):
        self._axis_params.near_position = self.getNearPosition()

    def getNearPosition(self):
        return float(self._qleNearPosQLE.text())

    def setNearPosition(self, position):
        self._qleNearPosQLE.setText(str(position))

    def setMode(self, mode):
        index = self._qcbPosition.findText(mode.value)
        if index >= 0:
            self._qcbPosition.setCurrentIndex(index)

    def setAxisParams(self, axis):
        old = self.blockSignals(True)
        if self._axis_params is not None:
            self._axis_params.sigChanged.disconnect(self._axis_params_changed)
        self._axis_params = axis
        self._axis_params.sigChanged.connect(self._axis_params_changed)
        self._axis_params_changed()
        self.blockSignals(old)

    def _axis_params_changed(self, *args, **kwargs):
        self.setMode(self._axis_params.mode)
        self.setNearPosition(self._axis_params.near_position)


class _InputWidget(qt.QWidget):
    __doc__ = 'Widget used to define the radio to use for axis calculation from\n    radios'

    def __init__(self, parent=None, axis_params=None):
        assert isinstance(axis_params, QAxisRP)
        qt.QWidget.__init__(self, parent)
        self.setLayout(qt.QVBoxLayout())
        self._angleModeWidget = _AngleModeGroupBox(parent=self, axis_params=axis_params)
        self.layout().addWidget(self._angleModeWidget)
        self._axisRadioUrlsWidget = _AxisUrlWidget(parent=self, axis_params=axis_params)
        self.layout().addWidget(self._axisRadioUrlsWidget)
        self._axis_params = axis_params
        self._axisRadioUrlsWidget.setEnabled(self._angleModeWidget._qrbCOR_manual.isChecked())
        self._angleModeWidget._qrbCOR_manual.toggled.connect(self._axisRadioUrlsWidget.setEnabled)
        self.setUrls = self._axisRadioUrlsWidget.setUrls
        self.setScanRange = self._angleModeWidget.setScanRange

    def setAxisParams(self, axis_params):
        self._angleModeWidget.setAxisParams(axis_params)
        self._axisRadioUrlsWidget.setAxisParams(axis_params)
        self._axis_params = axis_params


class _AngleModeGroupBox(qt.QGroupBox):
    __doc__ = 'Group box to select the angle to used for cor calculation\n    (0-180, 90-270 or manual)'

    def __init__(self, parent=None, axis_params=None):
        assert isinstance(axis_params, QAxisRP)
        qt.QGroupBox.__init__(self, parent=parent, title='Angles to use for axis calculation')
        self._corButtonsGps = qt.QButtonGroup(parent=self)
        self._corButtonsGps.setExclusive(True)
        self.setLayout(qt.QGridLayout())
        self._qrbCOR_0_180 = qt.QRadioButton('0-180', parent=self)
        self.layout().addWidget(self._qrbCOR_0_180, 0, 0)
        self._qrbCOR_90_270 = qt.QRadioButton('90-270', parent=self)
        self._qrbCOR_90_270.setToolTip('pick radio closest to angles 90° and 270°. If disable mean that the scan range is 180°')
        self.layout().addWidget(self._qrbCOR_90_270, 0, 1)
        self._qrbCOR_manual = qt.QRadioButton('manual selection', parent=self)
        self._qrbCOR_manual.setVisible(False)
        self.layout().addWidget(self._qrbCOR_manual, 0, 2)
        for b in (self._qrbCOR_0_180, self._qrbCOR_90_270,
         self._qrbCOR_manual):
            self._corButtonsGps.addButton(b)

        self.setAxisParams(axis_params)
        self._corButtonsGps.buttonClicked.connect(self._angleModeChanged)

    def setScanRange(self, scanRange):
        if scanRange == 180:
            self._qrbCOR_90_270.setEnabled(False)
            if self._qrbCOR_90_270.isChecked():
                self._qrbCOR_0_180.setChecked(True)

    def setAngleMode(self, mode):
        """"

        :param mode: mode to use (can be manual , 90-270 or 0-180)
        """
        if not isinstance(mode, CorAngleMode):
            raise AssertionError
        elif mode == CorAngleMode.use_0_180:
            self._qrbCOR_0_180.setChecked(True)
        else:
            if mode == CorAngleMode.use_90_270:
                self._qrbCOR_90_270.setChecked(True)
            else:
                self._qrbCOR_manual.setChecked(True)

    def getAngleMode(self):
        """

        :return: the angle to use for the axis calculation
        :rtype: CorAngleMode
        """
        if self._qrbCOR_90_270.isChecked():
            return CorAngleMode.use_90_270
        if self._qrbCOR_0_180.isChecked():
            return CorAngleMode.use_0_180
        return CorAngleMode.manual_selection

    def setAxisParams(self, axis_params):
        old = self.blockSignals(True)
        self._axis_params = axis_params
        self.setAngleMode(axis_params.angle_mode)
        self.blockSignals(old)

    def _angleModeChanged(self, *args, **kwargs):
        self._axis_params.angle_mode = self.getAngleMode()


class _AxisUrlWidget(qt.QWidget):
    __doc__ = '\n    Widget used to show url the user can select for computing axis position\n    '
    _RADIO_1_NAME = 'radio 1'
    _RADIO_2_NAME = 'radio 2'

    def __init__(self, parent=None, axis_params=None):
        qt.QWidget.__init__(self, parent=parent)
        assert isinstance(axis_params, QAxisRP)
        self._recons_params = axis_params
        self._scan = None
        self._scan_proj_urls = None
        self.setLayout(qt.QGridLayout())
        self.layout().addWidget(qt.QLabel((self._RADIO_1_NAME), parent=self), 0, 0)
        self.layout().addWidget(qt.QLabel((self._RADIO_2_NAME), parent=self), 1, 0)
        self._url1QLE = qt.QLineEdit(parent=self)
        self.layout().addWidget(self._url1QLE, 0, 1, 1, 2)
        self._url2QLE = qt.QLineEdit(parent=self)
        self.layout().addWidget(self._url2QLE, 1, 1, 1, 2)
        self._selectButton = qt.QPushButton('select', parent=self)
        self.layout().addWidget(self._selectButton, 2, 2)
        self._selectButton.hide()
        spacer = qt.QWidget(parent=self)
        spacer.setSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Expanding)
        self.layout().addWidget(spacer, 3, 0)
        columns = OrderedDict([
         (
          self._RADIO_1_NAME, ColumnMode.SINGLE),
         (
          self._RADIO_2_NAME, ColumnMode.SINGLE)])
        self._urlSelectionTable = UrlSelectionDialog(columns=columns, parent=None)
        self._selectButton.clicked.connect(self._selectUrls)
        self._url1QLE.editingFinished.connect(self._url1Updated)
        self._url2QLE.editingFinished.connect(self._url2Updated)

    def _url1Updated(self):
        from silx.io.url import DataUrl
        try:
            url = DataUrl(path=(self._url1QLE.text()))
        except:
            _logger.info('fail to create an url out of', self._url1QLE.text())
        else:
            self._scan.axis_params.axis_url_1 = url

    def _url2Updated(self):
        from silx.io.url import DataUrl
        try:
            url = DataUrl(path=(self._url2QLE.text()))
        except:
            _logger.info('fail to create an url out of', self._url2QLE.text())
        else:
            self._scan.axis_params.axis_url_2 = url

    def _updateAxisFiles(self, scan):
        assert scan is not None
        self._scan = scan
        if scan.axis_params is not None:
            if scan.axis_params.n_url() == 2:
                axis = scan.axis_params
                self.updateUrl1Value(prop=(axis.axis_url_1.url))
                self.updateUrl2Value(prop=(axis.axis_url_2.url))

    def updateUrl1Value(self, prop):
        old = self.blockSignals(True)
        self._updateAxisValue(qle=(self._url1QLE), prop=prop)
        self.blockSignals(old)

    def updateUrl2Value(self, prop):
        old = self.blockSignals(True)
        self._updateAxisValue(qle=(self._url2QLE), prop=prop)
        self.blockSignals(old)

    def _updateAxisValue(self, qle, prop):
        if prop is None:
            value = ''
        else:
            value = prop.path()
        qle.setText(value)

    def setUrls(self, scan):
        """
        Update the interface to fit to the given scan and urls

        :param TomoBase scan:
        """
        if not scan is not None:
            raise AssertionError
        else:
            if self._scan is None or self._scan.path != scan.path:
                self._scan = scan
                self._scan_proj_urls = scan.getProjectionsUrl()
            self._updateAxisFiles(scan=scan)
            if scan.axis_params is not None:
                n_url = scan.axis_params.n_url()
                if n_url >= 1:
                    url1 = scan.axis_params.axis_url_1.url
                    self._urlSelectionTable.addUrl(url1)
                if n_url >= 2:
                    url2 = scan.axis_params.axis_url_2.url
                    self._urlSelectionTable.addUrl(url2)
        self._scan = scan

    def _selectUrls(self):
        assert self._scan
        assert self._scan.axis_params
        proj_urls = self._scan.getProjectionsUrl()
        self._urlSelectionTable.setUrls(proj_urls.values())
        axis = self._scan.axis_params
        sel_url_1 = None
        if axis.axis_url_1 is not None:
            sel_url_1 = [
             axis.axis_url_1.url]
        sel_url_2 = None
        if axis.axis_url_2 is not None:
            sel_url_2 = [
             axis.axis_url_2.url]
        selection = {self._RADIO_1_NAME: sel_url_1, 
         self._RADIO_2_NAME: sel_url_2}
        self._urlSelectionTable.setSelection(selection=selection)
        if self._urlSelectionTable.exec_():
            selection = self._urlSelectionTable.getSelection()

            def apply_selection(sel_name):
                sel = selection[sel_name]
                if sel is not None:
                    assert len(sel) is 1
                    sel = sel[0]
                return sel

            sel = apply_selection(self._RADIO_1_NAME)
            self._scan.axis_params.axis_url_1 = sel
            self.updateUrl1Value(sel)
            sel = apply_selection(self._RADIO_2_NAME)
            self._scan.axis_params.axis_url_2 = sel
            self.updateUrl2Value(sel)

    def setAxisParams(self, axis):
        self._recons_params = axis