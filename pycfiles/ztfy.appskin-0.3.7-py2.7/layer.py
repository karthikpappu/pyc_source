# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/appskin/layer.py
# Compiled at: 2013-04-23 02:36:24
__docformat__ = 'restructuredtext'
from ztfy.bootstrap.layer import IBootstrapLayer, IBootstrapSkin
from zope.schema import TextLine
from ztfy.appskin import _

class IAppLayer(IBootstrapLayer):
    """Application base layer"""
    pass


class IAppSkin(IAppLayer, IBootstrapSkin):
    """Application base skin"""
    label = TextLine(title=_('ZTFY application skin'))