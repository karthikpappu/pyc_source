# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/polygot/tests/test_print.py
# Compiled at: 2016-10-08 10:29:41
import os, nose, shutil, yaml
from polygot.utKit import utKit
stream = file('/Users/Dave/.config/polygot/polygot.yaml', 'r')
settings = yaml.load(stream)
stream.close()
moduleDirectory = os.path.dirname(__file__)
utKit = utKit(moduleDirectory)
log, dbConn, pathToInputDir, pathToOutputDir = utKit.setupModule()
utKit.tearDownModule()
try:
    shutil.rmtree(pathToOutputDir)
except:
    pass

if not os.path.exists(pathToOutputDir):
    os.makedirs(pathToOutputDir)

class test_printpdf:

    def test_printpdf_function(self):
        from polygot import printpdf
        pdf = printpdf(log=log, settings=settings, url='https://en.wikipedia.org/wiki/Volkswagen', folderpath=pathToOutputDir, title=False, append=False, readability=True).get()

    def test_printpdf_original_function(self):
        from polygot import printpdf
        pdf = printpdf(log=log, settings=settings, url='https://en.wikipedia.org/wiki/Volkswagen', folderpath=pathToOutputDir, title=False, append='_original', readability=False).get()

    def test_printpdf_original_rename_function(self):
        from polygot import printpdf
        pdf = printpdf(log=log, settings=settings, url='https://en.wikipedia.org/wiki/Volkswagen', folderpath=pathToOutputDir, title='Cars', append='_original', readability=False).get()