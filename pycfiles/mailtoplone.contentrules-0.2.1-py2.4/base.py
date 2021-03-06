# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/mailtoplone/contentrules/tests/base.py
# Compiled at: 2008-02-29 08:26:12
__author__ = 'Hans-Peter Locher <hans-peter.locher@inquant.de>'
__docformat__ = 'plaintext'
from Products.Five import zcml
from Products.Five import fiveconfigure
from Testing import ZopeTestCase as ztc
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup

@onsetup
def setup_mailtoplone_contentrules():
    """Set up mailtoplone base + contentrules
    """
    fiveconfigure.debug_mode = True
    import mailtoplone.contentrules, mailtoplone.base
    zcml.load_config('configure.zcml', mailtoplone.contentrules)
    zcml.load_config('configure.zcml', mailtoplone.base)
    fiveconfigure.debug_mode = False
    ztc.installPackage('mailtoplone.base')
    ztc.installPackage('mailtoplone.contentrules')


setup_mailtoplone_contentrules()
ptc.setupPloneSite(products=['mailtoplone.base', 'mailtoplone.contentrules'])

class MailToPloneContentrulesTestCase(ptc.PloneTestCase):
    """Base class used for test cases
    """
    __module__ = __name__


class MailToPloneContentrulesFunctionalTestCase(ptc.FunctionalTestCase):
    """Test case class used for functional (doc-)tests
    """
    __module__ = __name__