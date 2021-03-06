# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pycrud/controllers/archive.py
# Compiled at: 2008-06-20 03:40:59
import logging
from message import *
log = logging.getLogger(__name__)

class ArchiveController(MessageController):

    def _init_custom(self):
        c.columns_shown = [
         'sender',
         'recipient',
         'message',
         'created']
        c.column_descriptions['created'] = 'Received'

    def _list(self):
        c.entries = self.query.filter_by(folder=2)