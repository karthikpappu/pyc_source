# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/solstice/managers/menu.py
# Compiled at: 2020-03-08 13:23:53
# Size of source mod 2**32: 2314 bytes
"""
Module that contains manager that handles Solstice DCC Menu
"""
from __future__ import print_function, division, absolute_import
__author__ = 'Tomas Poveda'
__license__ = 'MIT'
__maintainer__ = 'Tomas Poveda'
__email__ = 'tpovedatd@gmail.com'
import webbrowser
from Qt.QtWidgets import *
import tpDcc
from tpDcc.libs.python import decorators
from tpDcc.libs.qt.core import qtutils
import artellapipe, artellapipe.register
from artellapipe.managers import menus
import artellapipe.libs.kitsu as kitsu_lib

class SolsticeMenu(menus.ArtellaMenusManager, object):

    def __init__(self):
        super(SolsticeMenu, self).__init__()

    def create_menus(self, package_name, project):
        valid_creation = super(SolsticeMenu, self).create_menus(package_name=package_name, project=project)
        if not valid_creation:
            artellapipe.logger.warning('Something went wrong during the creation of SolsticeMenu Menu')
            return False
        else:
            return self.create_kitsu_menu()

    def create_kitsu_menu(self):
        parent_menu_bar = qtutils.get_window_menu_bar(tpDcc.Dcc.get_main_window())
        if not parent_menu_bar:
            return
        else:
            kitsu_menu_name = 'kitsu_menu'
            for child_widget in parent_menu_bar.children():
                if child_widget.objectName() == kitsu_menu_name:
                    child_widget.deleteLater()

            self._kitsu_action = QAction(self._parent.menuBar())
            self._kitsu_action.setIcon(tpDcc.ResourcesMgr().icon('kitsu'))
            self._parent.menuBar().addAction(self._kitsu_action)
            self._kitsu_action.setObjectName(kitsu_menu_name)
            self._kitsu_action.triggered.connect(self._on_kitsu_open)
            return True

    def _on_kitsu_open(self):
        """
        Internal callback function that is called when kitsu action is pressed
        """
        project_url = kitsu_lib.config.get('project_url', None)
        if not project_url:
            return
        webbrowser.open(project_url)


@decorators.Singleton
class SolsticeMenuManagerSingleton(SolsticeMenu, object):

    def __init__(self):
        SolsticeMenu.__init__(self)


artellapipe.register.register_class('MenusMgr', SolsticeMenuManagerSingleton)