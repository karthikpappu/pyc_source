# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pypreval/store.py
# Compiled at: 2008-02-21 08:15:02
"""
"""
from __future__ import absolute_import
from .nulllock import NullLock
from .util import optional_makedirs
import os, cPickle

class Store(object):
    """This object manages the root object and all transactions"""
    lock_manager = NullLock
    transaction_per_directory = 512

    def _make_name(self, *name):
        """returns a path inside the storage directory."""
        return os.path.join(self._directory, *name)

    def _make_transaction_path(self, id):
        """returns the path for transaction id."""
        dir_id = int(id / self.transaction_per_directory)
        dir_name = self._make_name('t%07d' % dir_id)
        optional_makedirs(dir_name)
        return os.path.join(dir_name, '%08d' % id)

    def __init__(self, directory):
        self._lock = self.__class__.lock_manager()
        self._transid = 0
        self._directory = directory
        optional_makedirs(directory)
        self.root = None
        self._load_snapshot()
        self._replay_transactions()
        return

    def _load_snapshot(self):
        """This function loads the latest snapshot (if any) found in the directory"""
        names = [ (int(name[5:]), name) for name in os.listdir(self._directory) if name.startswith('snap.') ]
        if names:
            names.sort()
            latest_snapshot_name = names[(-1)][1]
            file_obj = file(os.path.join(self._directory, latest_snapshot_name), 'rb')
            (self._transid, self.root) = cPickle.load(file_obj)
            file_obj.close()
        else:
            self._transid = 0
            self.root = None
        return

    def _replay_transactions(self):
        while True:
            file_name = self._make_transaction_path(self._transid)
            if os.path.exists(file_name):
                file_obj = file(file_name, 'rb')
                transaction = cPickle.load(file_obj)
                file_obj.close()
                transaction(self)
                self._transid += 1
            else:
                break

    def submit_transaction(self, transaction):
        self._lock.acquire()
        try:
            if callable(getattr(transaction, 'prepare', None)):
                transaction.prepare(self)
            file_name = self._make_transaction_path(self._transid)
            file_obj = file(file_name, 'wb')
            transaction._transid = self._transid
            cPickle.dump(transaction, file_obj)
            file_obj.close()
            transaction(self)
            self._transid += 1
        finally:
            self._lock.release()

        return

    def save_snapshot(self):
        """This function takes the current state and creates a new snapshot."""
        self._lock.acquire()
        try:
            snap_name = self._make_name('snap.%d' % self._transid)
            file_obj = file(snap_name, 'wb')
            cPickle.dump((self._transid, self.root), file_obj)
            file_obj.close()
        finally:
            self._lock.release()