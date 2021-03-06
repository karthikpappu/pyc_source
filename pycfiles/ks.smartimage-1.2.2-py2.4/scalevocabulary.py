# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ks/smartimage/smartimagecache/scalevocabulary.py
# Compiled at: 2008-12-23 17:55:59
"""ScaleWidgets for the Zope 3 based smartimagecache package

$Id: scalevocabulary.py 12472 2007-10-26 19:21:11Z anton $
"""
__author__ = 'Addrey Orlov'
__license__ = 'ZPL'
__version__ = '$Revision: 12472 $'
__date__ = '$Date: 2007-10-26 22:21:11 +0300 (Fri, 26 Oct 2007) $'
from zope.schema.vocabulary import SimpleVocabulary

def ScaleVocabulary(context):
    return SimpleVocabulary.fromValues([ scale.name for scale in context.scales ])