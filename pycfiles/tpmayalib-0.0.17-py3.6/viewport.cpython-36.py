# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpMayaLib/core/viewport.py
# Compiled at: 2020-01-16 21:52:40
# Size of source mod 2**32: 5101 bytes
"""
This module defines class for Maya viewport widgets
"""
from __future__ import print_function, division, absolute_import
import os, logging, tempfile
from Qt.QtWidgets import *
import tpMayaLib as maya
from tpMayaLib.core import gui
LOGGER = logging.getLogger()

class MayaViewport(QWidget):

    def __init__(self, name='maya_viewport', label='Default Viewport', parent=None):
        super(MayaViewport, self).__init__(parent=parent)
        self._temp_file = tempfile.NamedTemporaryFile(mode='wb', suffix='.png', delete=False)
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.main_layout.setObjectName('viewport_main_layout')
        self.setLayout(self.main_layout)
        self.name = name
        self.label = label
        maya.cmds.setParent('|')
        pane_layout_name = maya.cmds.paneLayout(self.name)
        self.pane_layout = gui.to_qt_object(pane_layout_name)
        self.camera_name = maya.cmds.camera()[0]
        maya.cmds.hide(self.camera_name)
        self.model_panel_name = maya.cmds.modelPanel(label=(self.label), camera=(self.camera_name), menuBarVisible=False)
        maya.mel.eval('modelPanelBarDecorationsCallback("GridBtn","' + self.model_panel_name + '", "' + self.model_panel_name + '|modelEditorIconBar");')
        self.model_panel = gui.to_qt_object(self.model_panel_name)
        self.main_layout.addWidget(self.pane_layout)
        self._original_line_width = maya.cmds.modelEditor((self.model_panel_name), query=True, lineWidth=True)
        maya.cmds.modelEditor((self.model_panel_name), edit=True, displayAppearance='smoothShaded', lw=2)
        maya.cmds.viewFit((self.camera_name), all=False)
        self.collapse_menu_bar(True)

    def update_viewport(self):
        super(MayaViewport, self).update_viewport()

    def clean(self):
        super(MayaViewport, self).clean()
        if maya.cmds.objExists(self.camera_name):
            maya.cmds.delete(self.camera_name)
        maya.cmds.modelEditor((self.model_panel_name), edit=True, displayAppearance='smoothShaded', lw=(self._original_line_width))
        maya.cmds.modelPanel((self.model_panel_name), edit=True, unParent=True)
        maya.cmds.deleteUI((self.model_panel_name), panel=True)

    def create_snapshot(self, filename=None, size=None, **kwargs):
        """
        Implements create_snapshot abstract function
        :param filename: str, Path where the snapshot will be stored
        :param size: tuple<int, int>, tuple defining size and width of the image. If None, the complete width and height of the viewport will be used
        :param focus; bool, True if you want to focus to the model panel before taking the snapshot
        :return: str, Path where the snapshot has been stored or None if some error happens during snapshot
        """
        if filename is None:
            filename = self._temp_file.file.name
        else:
            focus = kwargs.get('focus', False)
            if focus:
                maya.cmds.setFocus(self.model_panel_name)
            try:
                if size:
                    f = maya.cmds.playblast(wh=(size[0], size[1]), fp=0, frame=maya.cmds.currentTime(query=True), format='image', compression='png', forceOverwrite=True, viewer=False)
                else:
                    f = maya.cmds.playblast(fp=0, frame=maya.cmds.currentTime(query=True), format='image', compression='png', forceOverwrite=True, viewer=False)
            except Exception as e:
                LOGGER.error(str(e))
                return

        f = os.path.abspath(f.replace('####', '0'))
        try:
            os.rename(f, filename + '.png')
        except Exception as e:
            LOGGER.error(str(e))
            return

        return os.path.abspath(filename)

    def collapse_menu_bar(self, value):
        """
        Sets the collapsed state for the menu bar of the Maya viewport
        :param value: bool, True if you want to collapse the menu bar or False otherwise
        """
        bar_layout = self._get_bar_layout()
        if maya.cmds.frameLayout(bar_layout, query=True, exists=True):
            maya.cmds.frameLayout(bar_layout, edit=True, collapse=value)

    def _get_bar_layout(self):
        """
        Returns the bar layout associated to the Maya viewport
        :return: unicode, bar layout name
        """
        bar_layout = maya.cmds.modelPanel((self.model_panel_name), query=True, barLayout=True)
        return bar_layout