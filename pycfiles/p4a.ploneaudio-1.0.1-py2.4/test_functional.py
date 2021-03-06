# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/p4a/ploneaudio/tests/test_functional.py
# Compiled at: 2007-11-27 10:18:04
import os, unittest, doctest
from zope.testing import doctestunit
from p4a import ploneaudio
import p4a.audio.tests
from p4a.ploneaudio.tests import testing
from Testing.ZopeTestCase.zopedoctest import ZopeDocFileSuite
from Testing.ZopeTestCase import FunctionalDocFileSuite
from App import Common
from Products.PloneTestCase import layer

def test_suite():
    suite = unittest.TestSuite()
    if __name__ not in ('__main__', 'p4a.ploneaudio.tests.test_functional'):
        return suite
    if ploneaudio.has_ataudio_support():
        from p4a.ploneaudio.ataudio import ataudiotests
        suite.addTest(ataudiotests.test_suite())
    if ploneaudio.has_fatsyndication_support():
        suite.addTest(ZopeDocFileSuite('syndication-integration.txt', package='p4a.ploneaudio', test_class=testing.IntegrationTestCase, optionflags=doctest.ELLIPSIS))
    suite.addTest(doctestunit.DocFileSuite('media-player.txt', package='p4a.audio'))
    suite.addTest(doctestunit.DocFileSuite('migration.txt', package='p4a.audio'))
    suite.addTest(ZopeDocFileSuite('plone-audio.txt', package='p4a.ploneaudio', test_class=testing.testclass_builder(file_type='File')))
    suite.addTest(FunctionalDocFileSuite('browser.txt', package='p4a.ploneaudio', test_class=testing.testclass_builder()))
    pkg_home = Common.package_home({'__name__': 'p4a.audio.tests'})
    samplesdir = os.path.join(pkg_home, 'samples')
    fields = dict(title='Test of the Emercy Broadcast System', artist='Rocky Burt', album='Emergencies All Around Us')
    SAMPLES = (
     (
      os.path.join(samplesdir, 'test-full.mp3'), 'audio/mpeg', fields), (os.path.join(samplesdir, 'test-full.ogg'), 'application/ogg', fields), (os.path.join(samplesdir, 'test-no-images.mp3'), 'audio/mpeg', fields))
    for (samplefile, mimetype, fields) in SAMPLES:
        suite.addTest(ZopeDocFileSuite('plone-audio-impl.txt', package='p4a.ploneaudio', test_class=testing.testclass_builder(samplefile=samplefile, required_mimetype=mimetype, file_content_type='File', fields=fields)))

    if ploneaudio.has_blobfile_support():
        (samplefile, mimetype, fields) = SAMPLES[0]
        suite.addTest(ZopeDocFileSuite('plone-audio-impl.txt', package='p4a.ploneaudio', test_class=testing.testclass_builder(samplefile=samplefile, required_mimetype=mimetype, file_content_type='BlobFile', fields=fields)))
    suite.layer = layer.ZCMLLayer
    return suite