# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cantools/web/dez_server/controller.py
# Compiled at: 2019-09-16 00:28:00
import sys, platform
from dez.network import SocketController, daemon_wrapper
from dez.logging import get_logger_getter
from cantools import config
from .daemons import Web, Admin
from .response import Response
from .cron import Cron
from cantools import config, __version__
from ..util import *
from ...util import log as syslog
logger_getter = get_logger_getter('httpd', syslog, config.log.allow)
CTR = None

class DController(SocketController):

    def __init__(self, *args, **kwargs):
        self.logger = logger_getter('Controller')
        SocketController.__init__(self, *args, **kwargs)
        self.handlers = {}
        self.logger.info('cantools: %s' % (__version__,))
        self.logger.info('Python: %s' % (sys.version.split(' ')[0],))
        self.logger.info('System: ' + (' > ').join([ part for part in platform.uname() if part ]))

    def _respond(self, resp, *args, **kwargs):
        if resp:
            kwargs['response'] = resp
            localvars.response = resp
        else:
            kwargs['noLoad'] = True
            kwargs['threaded'] = True
        do_respond(*args, **kwargs)

    def register_handler(self, args, kwargs):
        self.logger.info('register handler: %s' % (self.curpath,))
        self.handlers[self.curpath] = lambda resp: self._respond(resp, *args, **kwargs)

    def trigger_handler(self, rule, target, req=None):
        self.curpath = rule
        if rule not in self.handlers:
            self.logger.info('importing module: %s' % (target,))
            __import__(target)
        self.handlers[rule](req and Response(req))


def getController():
    global CTR
    if not CTR:
        CTR = DController()
        CTR.web = CTR.register_address(config.web.host, config.web.port, dclass=daemon_wrapper(Web, logger_getter))
        CTR.web.controller = CTR
        config.admin.update('pw', config.cache('admin password? ', overwrite=config.newpass))
        CTR.admin = CTR.register_address(config.admin.host, config.admin.port, dclass=daemon_wrapper(Admin, logger_getter))
        CTR.admin.controller = CTR
        Cron(CTR, logger_getter)
    return CTR