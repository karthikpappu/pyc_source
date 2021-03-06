# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web2ldap/app/core.py
# Compiled at: 2020-05-04 07:51:59
# Size of source mod 2**32: 2522 bytes
"""
web2ldap.app.core: some core functions used throughout web2ldap

web2ldap - a web-based LDAP Client,
see https://www.web2ldap.de for details

(c) 1998-2020 by Michael Stroeder <michael@stroeder.com>

This software is distributed under the terms of the
Apache License Version 2.0 (Apache-2.0)
https://www.apache.org/licenses/LICENSE-2.0
"""
import sys, os, time, web2ldap.__about__
from web2ldap.log import logger
OS_SYS_PREFIXES = {
 '/usr',
 '/usr/local'}
logger.info('Starting web2ldap %s', web2ldap.__about__.__version__)
os.environ['LDAPNOINIT'] = '1'
logger.debug('Disabled processing .ldaprc or ldap.conf (LDAPNOINIT=%s)', os.environ['LDAPNOINIT'])
import ldap0
from web2ldap.checkinst import check_inst
check_inst()
if 'WEB2LDAP_HOME' in os.environ:
    etc_dir = os.path.join(os.environ['WEB2LDAP_HOME'], 'etc', 'web2ldap')
else:
    if os.name == 'posix' and sys.prefix in OS_SYS_PREFIXES:
        etc_dir = '/etc/web2ldap'
    else:
        etc_dir = os.path.join(sys.prefix, 'etc', 'web2ldap')
templates_dir = os.path.join(etc_dir, 'templates')
sys.path.append(etc_dir)
import web2ldapcnf, web2ldapcnf.hosts, web2ldap.app.cnf

class ErrorExit(Exception):
    __doc__ = 'Base class for web2ldap application exceptions'

    def __init__(self, Msg):
        assert isinstance(Msg, str), TypeError("Type of argument 'Msg' must be str, was %r" % Msg)
        self.Msg = Msg


logger.debug('End of module %s', __name__)
from warnings import filterwarnings
filterwarnings(action='error', category=UnicodeWarning)
ldap0._trace_level = web2ldapcnf.ldap_trace_level
ldap0.set_option(ldap0.OPT_DEBUG_LEVEL, web2ldapcnf.ldap_opt_debug_level)
ldap0.set_option(ldap0.OPT_RESTART, 0)
ldap0.set_option(ldap0.OPT_DEREF, 0)
ldap0.set_option(ldap0.OPT_REFERRALS, 0)
STARTUP_TIME = time.time()