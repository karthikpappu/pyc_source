# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/martijndevos/Documents/anydex-core/anydex/core/transaction_manager.py
# Compiled at: 2019-06-08 04:52:20
import logging
from anydex.core.payment import Payment
from anydex.core.timestamp import Timestamp
from anydex.core.transaction import Transaction
from anydex.core.transaction_repository import TransactionRepository

class TransactionManager(object):
    """Manager for retrieving and creating transactions"""

    def __init__(self, transaction_repository):
        """
        :type transaction_repository: TransactionRepository
        """
        super(TransactionManager, self).__init__()
        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.info('Transaction manager initialized')
        self.transaction_repository = transaction_repository

    def find_by_id(self, transaction_id):
        """
        :param transaction_id: The transaction id to look for
        :type transaction_id: TransactionId
        :return: The transaction or null if it cannot be found
        :rtype: Transaction
        """
        return self.transaction_repository.find_by_id(transaction_id)

    def find_all(self):
        """
        :rtype: [Transaction]
        """
        return self.transaction_repository.find_all()