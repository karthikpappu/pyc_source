# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/base/gui/plugins/BaseZipImport.py
# Compiled at: 2019-12-11 16:37:39
"""Plugin to import selected card sets from a zip file"""
import os
from logging import Logger
import gtk, gobject
from ..BasePluginManager import BasePlugin
from ..SutekhDialog import SutekhDialog, do_complaint_error, do_exception_complaint
from ..SutekhFileWidget import ZipFileDialog
from ..ProgressDialog import ProgressDialog, SutekhCountLogHandler
from ..ScrolledList import ScrolledList
from ..GuiCardSetFunctions import reparent_all_children, update_open_card_sets, get_import_name, PROMPT, RENAME, REPLACE

def _do_rename_parent(sOldName, sNewName, dRemaining):
    """Handle the renaming of a parent card set in the unprocessed list."""
    dResult = {}
    for sName, tInfo in dRemaining.iteritems():
        if tInfo[3] == sOldName:
            dResult[sName] = (
             tInfo[0], tInfo[1], tInfo[2], sNewName)
        else:
            dResult[sName] = tInfo

    return dResult


def _set_selected_rows(_oButton, oScrolledList, aData):
    """Helper to manage changing the se;ection of the scrolled list"""
    oScrolledList.set_selected_rows(aData)


class ZipFileDirStore(gtk.TreeStore):
    """Simple tree store to show card set hierachy in a ScrolledList widget"""

    def __init__(self):
        super(ZipFileDirStore, self).__init__(gobject.TYPE_STRING)

    def fill_list(self, dEscapedList):
        """Fill the list"""
        self.clear()
        aNames = sorted(dEscapedList)
        dAdded = {}
        while aNames:
            for sEntry in aNames[:]:
                sParent = dEscapedList[sEntry][3]
                if sParent:
                    sParent = gobject.markup_escape_text(sParent)
                oIter = None
                if sParent in dAdded:
                    oParIter = dAdded[sParent]
                    oIter = self.append(oParIter)
                elif sParent is None or sParent not in aNames:
                    oIter = self.append(None)
                else:
                    continue
                self.set(oIter, 0, sEntry)
                dAdded[sEntry] = oIter
                aNames.remove(sEntry)

        self.set_sort_column_id(0, gtk.SORT_ASCENDING)
        return


class SelectZipFileContents(SutekhDialog):
    """Dialog for querying contents of the zip file"""

    def __init__(self, dEscapedList, oParent):
        super(SelectZipFileContents, self).__init__('Select Card Sets to Import', oParent, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, (
         gtk.STOCK_OK, gtk.RESPONSE_OK,
         gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL))
        self.dEscapedList = dEscapedList
        oModel = ZipFileDirStore()
        self.oScrolledList = ScrolledList('Available Card Sets', oModel)
        self.vbox.pack_start(self.oScrolledList)
        self.oScrolledList.set_size_request(450, 300)
        self.oScrolledList.fill_list(self.dEscapedList)
        self.oScrolledList.view.expand_all()
        oSelectAll = gtk.Button('Select All')
        oUnSelectAll = gtk.Button('Unselect All')
        oSelectAll.connect('clicked', _set_selected_rows, self.oScrolledList, self.dEscapedList)
        oUnSelectAll.connect('clicked', _set_selected_rows, self.oScrolledList, [])
        oSelectButtons = gtk.VBox(False, 2)
        oSelectButtons.pack_start(oSelectAll, expand=False)
        oSelectButtons.pack_start(oUnSelectAll, expand=False)
        self.oPrompt = gtk.RadioButton(None, 'Always Ask', False)
        self.oPrompt.set_active(True)
        self.oReplace = gtk.RadioButton(self.oPrompt, 'Always replace with new card set', False)
        self.oReplace.set_active(False)
        self.oRename = gtk.RadioButton(self.oPrompt, 'Always create unique name', False)
        self.oRename.set_active(False)
        oRadioButs = gtk.VBox(False, 2)
        oRadioLabel = gtk.Label()
        oRadioLabel.set_markup('<b>How to handle card set name conflicts?</b>')
        oRadioButs.pack_start(oRadioLabel)
        oRadioButs.pack_start(self.oPrompt, expand=False)
        oRadioButs.pack_start(self.oReplace, expand=False)
        oRadioButs.pack_start(self.oRename, expand=False)
        oButtons = gtk.HBox(False, 2)
        oButtons.pack_start(oSelectButtons, expand=False)
        oButtons.pack_start(oRadioButs)
        self.vbox.pack_start(oButtons, expand=False)
        self.show_all()
        return

    def get_clash_mode(self):
        """Return the selected clash mode"""
        if self.oRename.get_active():
            return RENAME
        if self.oReplace.get_active():
            return REPLACE
        return PROMPT

    def get_selected(self):
        """Get the list of selected card sets"""
        dSelected = {}
        for sName in self.oScrolledList.get_selection():
            dSelected[sName] = self.dEscapedList[sName]

        return dSelected


class BaseZipImport(BasePlugin):
    """Extract selected card sets from a zip file."""
    dTableVersions = {}
    aModelsSupported = ('MainWindow', )
    cZipWrapper = None
    sMenuName = 'Import Card Set(s) from zip file'
    sHelpCategory = 'card_list:file'
    sHelpText = 'This option allows you to select some or all of\n                   the Card Sets included in a zip file (such as those\n                   produced by backups) and import them into the database.\n                   Unlike restoring a backup, this does not replace any\n                   existing card sets automatically.\n\n                   After selecting the zip file, you will be asked to\n                   select the card sets to import from the list of card\n                   sets in the zip file. If any of the card sets share\n                   the same name as an existing card set, you will be\n                   asked either to rename the card set, or skip importing\n                   that card set.\n\n                   If a card set to be imported has a parent card set, and\n                   that set cannot be found, the card set will be imported\n                   with no parent set.'

    def get_menu_item(self):
        """Register on the Plugins menu"""
        oImport = gtk.MenuItem(self.sMenuName)
        oImport.connect('activate', self.make_dialog)
        return ('Import Card Set', oImport)

    def make_dialog(self, _oWidget):
        """Create the dialog used to select the zip file"""
        sName = 'Select zip file to import from.'
        oDlg = ZipFileDialog(self.parent, sName, gtk.FILE_CHOOSER_ACTION_OPEN)
        oDlg.show_all()
        oDlg.run()
        sFilename = oDlg.get_name()
        if sFilename:
            self.handle_response(sFilename)

    def handle_response(self, sFilename):
        """Handle response from the import dialog"""
        if not os.path.exists(sFilename):
            do_complaint_error('Backup file %s does not seem to exist.' % sFilename)
            return
        oFile = self.cZipWrapper(sFilename)
        dList = oFile.get_all_entries()
        dEscapedList = {}
        for sName, tInfo in dList.iteritems():
            dEscapedList[self._escape(sName)] = (
             sName, tInfo[0], tInfo[1],
             tInfo[2])

        oSelDlg = SelectZipFileContents(dEscapedList, self.parent)
        oResponse = oSelDlg.run()
        dSelected = oSelDlg.get_selected()
        iClashMode = oSelDlg.get_clash_mode()
        oSelDlg.destroy()
        if oResponse == gtk.RESPONSE_OK and dSelected:
            self.do_read_list(oFile, dSelected, iClashMode)

    def do_read_list(self, oFile, dSelected, iClashMode):
        """Read the selected list of card sets"""
        oLogHandler = SutekhCountLogHandler()
        oProgressDialog = ProgressDialog()
        oProgressDialog.set_description('Importing Files')
        oLogger = Logger('Read zip file')
        oLogger.addHandler(oLogHandler)
        oLogHandler.set_dialog(oProgressDialog)
        oLogHandler.set_total(len(dSelected))
        oProgressDialog.show()
        while dSelected:
            dSelected = self._read_heart(oFile, dSelected, oLogger, iClashMode)

        oProgressDialog.destroy()

    def _read_heart(self, oFile, dSelected, oLogger, iClashMode):
        """Heart of the reading loop - ensure we read parents before
           children, and correct for renames that occur."""
        dRemaining = {}
        dRenames = {}
        for sEscapedName, tInfo in dSelected.iteritems():
            sName, sFilename, bParentExists, sParentName = tInfo
            if sParentName is not None and sParentName in dSelected and sParentName not in dRenames:
                if not bParentExists:
                    dRemaining[sEscapedName] = (
                     sName, sFilename, True,
                     sParentName)
                else:
                    dRemaining[sEscapedName] = tInfo
                continue
            else:
                if sParentName is not None and sParentName in dRenames:
                    sParentName = dRenames[sParentName]
                elif not bParentExists:
                    sParentName = None
                try:
                    oCardSetHolder = oFile.read_single_card_set(sFilename)
                    oLogger.info('Read %s' % sName)
                    oCardSetHolder, aChildren = get_import_name(oCardSetHolder, iClashMode)
                    dRenames[sName] = oCardSetHolder.name
                    dRemaining = _do_rename_parent(sName, oCardSetHolder.name, dRemaining)
                    if not oCardSetHolder.name:
                        continue
                    oCardSetHolder.parent = sParentName
                    oCardSetHolder.create_pcs(self.cardlookup)
                    reparent_all_children(oCardSetHolder.name, aChildren)
                    if self.parent.find_cs_pane_by_set_name(oCardSetHolder.name):
                        update_open_card_sets(oCardSetHolder.name, self.parent)
                    self._reload_pcs_list()
                except Exception as oException:
                    sMsg = 'Failed to import card set %s.\n\n%s' % (sName,
                     oException)
                    do_exception_complaint(sMsg)

        return dRemaining