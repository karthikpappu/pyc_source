# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpMayaLib/core/sequencer.py
# Compiled at: 2020-01-16 21:52:40
# Size of source mod 2**32: 1711 bytes
"""
This module contains functions and classes to handle Maya Camera Sequencer functionality
"""
from __future__ import print_function, division, absolute_import
from Qt.QtWidgets import *
import tpMayaLib as maya

def open_camera_sequencer_window():
    """
    Opens Maya Camera Sequencer tool
    :return:
    """
    maya.cmds.SequenceEditor()


def close_camera_sequencer_window():
    """
    Closes Maya Camera Sequencer window
    """
    camera_sequencer_window = get_camera_sequencer_window()
    if not camera_sequencer_window:
        return
    camera_sequencer_window.close()


def get_camera_sequencer_window(try_to_open=True):
    """
    Returns Maya Camera Sequencer Window as a Qt widget
    :param try_to_open: bool, Whether to force the opening of the window if it is not already opened
    :return:QMainWindow or None
    """
    camera_sequencer_window = None
    widgets = QApplication.topLevelWidgets()
    for widget in widgets:
        widget_title = widget.windowTitle()
        if widget_title == 'Camera Sequencer':
            camera_sequencer_window = widget
            break

    if not camera_sequencer_window:
        open_camera_sequencer_window()
        if try_to_open:
            camera_sequencer_window = get_camera_sequencer_window(False)
    return camera_sequencer_window


def get_camera_sequencer_panel():
    """
    Returns Maya Camera Sequencer Panel as a QtWidget
    :return: QtWidget or None
    """
    from tpMayaLib.core import gui
    open_camera_sequencer_window()
    sequencer = maya.cmds.getPanel(scriptType='sequenceEditorPanel')[0]
    qt_obj = gui.to_qt_object(sequencer)
    return qt_obj