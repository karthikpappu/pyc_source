# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pycrud/controllers/delivery_confirm_old.py
# Compiled at: 2008-06-20 02:48:54
import logging
from pycrud.lib.base import *
from transaction import TransactionController
log = logging.getLogger(__name__)

class DeliveryConfirmController(TransactionController):

    def _list_query(self):
        self.query = model.Session.query(self.table).order_by(self.table.id.desc())
        self.query = self.query.filter_by(type=3)

    def render_edit(self):
        return render('/delivery_confirm/edit.mako')

    def _save_custom(self, params):
        entry = model.Session.query(model.StocksOut).filter_by(area=params['area']).filter_by(item=params['trans_item.item'])
        entry[0].qty -= int(params['trans_item.qty'])
        return params