# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/orangecontrib/tomwer/widgets/control/DataSelectorOW.py
# Compiled at: 2020-03-06 02:01:31
# Size of source mod 2**32: 3361 bytes
__authors__ = [
 'C. Nemoz', 'H. Payno']
__license__ = 'MIT'
__date__ = '25/05/2018'
from Orange.widgets import widget, gui
from Orange.widgets.widget import Output, Input
from tomwer.web.client import OWClient
from tomwer.gui.scanselectorwidget import ScanSelectorWidget
from tomwer.core.scan.scanbase import TomoBase
import logging
logger = logging.getLogger(__name__)

class DataSelectorOW(widget.OWWidget, OWClient):
    name = 'data selector'
    id = 'orange.widgets.tomwer.scanselector'
    description = 'List all received scan. Then user can select a specificscan to be passed to the next widget.'
    icon = 'icons/scanselector.svg'
    priority = 42
    category = 'esrfWidgets'
    keywords = ['tomography', 'selection', 'tomwer', 'folder']
    want_main_area = True
    resizing_enabled = True
    compress_signal = False

    class Inputs:
        data_in = Input(name='data', type=TomoBase)

    class Outputs:
        data_out = Output(name='data', type=TomoBase)

    def __init__(self, parent=None):
        """
        """
        widget.OWWidget.__init__(self, parent)
        OWClient.__init__(self, logger)
        self.widget = ScanSelectorWidget(parent=self)
        self.widget.sigSelectionChanged.connect(self.changeSelection)
        layout = gui.vBox(self.mainArea, self.name).layout()
        layout.addWidget(self.widget)
        self.setActiveScan = self.widget.setActiveScan

    @Inputs.data_in
    def addScan(self, scan):
        if scan:
            self.widget.add(scan)

    def changeSelection(self, list_scan):
        if list_scan:
            for scan_id in list_scan:
                if scan_id in self.widget.dataList._scanIDs:
                    scan = self.widget.dataList._scanIDs[scan_id]
                    assert isinstance(scan, TomoBase)
                    self.Outputs.data_out.send(scan)


if __name__ == '__main__':
    from silx.gui import qt
    qapp = qt.QApplication([])
    widget = DataSelectorOW(parent=None)
    widget.show()
    qapp.exec_()