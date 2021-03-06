# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.8.2-i386/egg/worldcookery/browser/adapter.py
# Compiled at: 2006-09-21 05:27:35
from zope.publisher.browser import BrowserLanguages

class BrowserFormLanguages(BrowserLanguages):
    __module__ = __name__

    def getPreferredLanguages(self):
        langs = super(BrowserFormLanguages, self).getPreferredLanguages()
        form_lang = self.request.get('ZopeLanguage', None)
        if form_lang is not None:
            langs.insert(0, form_lang)
        return langs