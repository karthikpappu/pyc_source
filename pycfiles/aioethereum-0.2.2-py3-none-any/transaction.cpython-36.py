# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/aioetcd3/transaction.py
# Compiled at: 2018-05-26 21:48:07
# Size of source mod 2**32: 1810 bytes
from aioetcd3._etcdv3 import rpc_pb2 as rpc
from aioetcd3.utils import to_bytes

class BaseCompare(object):

    def __init__(self, key):
        self.key = key
        self.value = None
        self.op = None

    def __eq__(self, other):
        self.value = other
        self.op = rpc.Compare.EQUAL
        return self

    def __ne__(self, other):
        self.value = other
        self.op = rpc.Compare.NOT_EQUAL
        return self

    def __lt__(self, other):
        self.value = other
        self.op = rpc.Compare.LESS
        return self

    def __gt__(self, other):
        self.value = other
        self.op = rpc.Compare.GREATER
        return self

    def __repr__(self):
        return "{}: {} {} '{}'".format(self.__class__, self.key, self.op, self.value)

    def build_message(self):
        compare = rpc.Compare()
        compare.key = to_bytes(self.key)
        if self.op is None:
            raise ValueError('op must be one of =, < or >')
        compare.result = self.op
        self.build_compare(compare)
        return compare

    def build_compare(self, compare):
        raise NotImplementedError


class Value(BaseCompare):

    def build_compare(self, compare):
        compare.target = rpc.Compare.VALUE
        compare.value = to_bytes(self.value)


class Version(BaseCompare):

    def build_compare(self, compare):
        compare.target = rpc.Compare.VERSION
        compare.version = int(self.value)


class Create(BaseCompare):

    def build_compare(self, compare):
        compare.target = rpc.Compare.CREATE
        compare.create_revision = int(self.value)


class Mod(BaseCompare):

    def build_compare(self, compare):
        compare.target = rpc.Compare.MOD
        compare.mod_revision = int(self.value)