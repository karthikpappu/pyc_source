# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/hvelarde/collective/behavior.richpreview/src/collective/behavior/richpreview/tests/test_controlpanel.py
# Compiled at: 2018-04-05 17:11:05
from collective.behavior.richpreview.config import PROJECTNAME
from collective.behavior.richpreview.interfaces import IRichPreviewSettings
from collective.behavior.richpreview.testing import INTEGRATION_TESTING
from plone import api
from plone.app.testing import logout
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
import unittest

class ControlPanelTestCase(unittest.TestCase):
    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.controlpanel = self.portal['portal_controlpanel']

    def test_controlpanel_has_view(self):
        view = api.content.get_view('richpreview-settings', self.portal, self.request)
        view = view.__of__(self.portal)
        self.assertTrue(view())

    def test_controlpanel_view_is_protected(self):
        from AccessControl import Unauthorized
        logout()
        with self.assertRaises(Unauthorized):
            self.portal.restrictedTraverse('@@richpreview-settings')

    def test_controlpanel_installed(self):
        actions = [ a.getAction(self)['id'] for a in self.controlpanel.listActions() ]
        self.assertIn('richpreview', actions)

    def test_controlpanel_removed_on_uninstall(self):
        qi = self.portal['portal_quickinstaller']
        with api.env.adopt_roles(['Manager']):
            qi.uninstallProducts(products=[PROJECTNAME])
        actions = [ a.getAction(self)['id'] for a in self.controlpanel.listActions() ]
        self.assertNotIn('richpreview', actions)


class RegistryTestCase(unittest.TestCase):
    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.registry = getUtility(IRegistry)
        self.settings = self.registry.forInterface(IRichPreviewSettings)

    def test_enable_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'enable'))
        self.assertEqual(self.settings.enable, True)

    def test_records_removed_on_uninstall(self):
        qi = self.portal['portal_quickinstaller']
        with api.env.adopt_roles(['Manager']):
            qi.uninstallProducts(products=[PROJECTNAME])
        records = [
         IRichPreviewSettings.__identifier__ + '.enable']
        for r in records:
            self.assertNotIn(r, self.registry)