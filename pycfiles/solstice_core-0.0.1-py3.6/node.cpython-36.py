# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/solstice/core/node.py
# Compiled at: 2019-10-05 11:59:30
# Size of source mod 2**32: 3220 bytes
"""
Module that contains definitions for DCC nodes in Solstice
"""
from __future__ import print_function, division, absolute_import
__author__ = 'Tomas Poveda'
__license__ = 'MIT'
__maintainer__ = 'Tomas Poveda'
__email__ = 'tpovedatd@gmail.com'
import tpDccLib as tp
from artellapipe.utils import resource
from artellapipe.core import node
from solstice.core import defines

class SolsticeAssetNode(node.ArtellaAssetNode, object):

    def __init__(self, project, node=None, **kwargs):
        (super(SolsticeAssetNode, self).__init__)(project=project, node=node, **kwargs)

    def get_icon(self):
        """
        Returns icon of the node depending of the type and extension
        :return: QIcon
        """
        if tp.Dcc.is_camera(self.name):
            return resource.ResourceManager().icon('camera')
        else:
            return self.get_current_extension_icon()

    def get_current_extension(self):
        """
        Overrides base ArtellaAsset get_current_extension function
        Returns the extension of the current asset file loaded
        :return: str
        """
        if self.is_rig():
            return defines.SOLSTICE_RIG_EXTENSION
        else:
            if self.is_alembic():
                return defines.SOLSTICE_ALEMBIC_EXTENSION
            return defines.SOLSTICE_STANDIN_EXTENSION

    def get_current_extension_icon(self):
        """
        Returns icon of the current asset extension
        :return: QIcon
        """
        current_extension = self.get_current_extension()
        if current_extension == defines.SOLSTICE_RIG_EXTENSION:
            return resource.ResourceManager().icon('rig')
        else:
            if current_extension == defines.SOLSTICE_ALEMBIC_EXTENSION:
                return resource.ResourceManager().icon('alembic')
            return resource.ResourceManager().icon('standin')

    def is_rig(self):
        """
        Returns whether current asset is a rig or not
        :return: bool
        """
        valid_tag_data = False
        main_group_connections = tp.Dcc.list_source_connections(node=(self._node))
        if not main_group_connections:
            return valid_tag_data
        else:
            for connection in main_group_connections:
                attrs = tp.Dcc.list_user_attributes(node=connection)
                if attrs and type(attrs) == list:
                    for attr in attrs:
                        if attr == 'tag_type':
                            valid_tag_data = True
                            break

            return valid_tag_data

    def is_alembic(self):
        """
        Returns whether current asset is an alembic or not
        :return: bool
        """
        valid_tag_data = False
        attrs = tp.Dcc.list_user_attributes(node=(self._node))
        if attrs:
            if type(attrs) == list:
                for attr in attrs:
                    if attr == 'tag_info':
                        valid_tag_data = True
                        break

        return valid_tag_data

    def is_standin(self):
        """
        Returns whether current asset is an standin or not
        :return: bool
        """
        raise NotImplementedError('is_standin functionality is not implemented yet!')