# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/gorgou/sql/mongo.py
# Compiled at: 2018-02-02 23:22:40
# Size of source mod 2**32: 3732 bytes
from pymongo import MongoClient
from pymongo import ASCENDING, DESCENDING
from gorgou.x import jsonx

class Connection(object):

    def __init__(self, mongo_conf_file=None):
        if not mongo_conf_file:
            mongo_conf_file = 'mongo.conf'
        mongo_conf = jsonx.load_json(mongo_conf_file)
        self.host = mongo_conf['host']
        self.user = mongo_conf['user']
        self.password = mongo_conf['passwd']
        self.database = mongo_conf['db']
        self.port = mongo_conf['port']
        connection_str = 'mongodb://' + str(self.user) + ':' + str(self.password) + '@' + str(self.host) + ':' + str(self.port) + '/' + str(self.database)
        self.connection = MongoClient(connection_str)

    @property
    def conn(self):
        return self.connection

    @conn.setter
    def conn(self, value):
        self.connection = value

    def get_db(self):
        return self.connection[self.database]

    def get_collection(self, table):
        return self.get_db()[table]

    def self_get(self, table, where=None):
        tb = self.get_collection(table)
        return tb.find(where)

    def get_all(self, table, where=None):
        return self.self_get(table, where)

    def get_all_tolist(self, table, where=None):
        return list(self.self_get(table, where))

    def count(self, table, where=None):
        return self.self_get(table, where).count()

    def get_page(self, table, where, sort, direction, pageSize, pageNum):
        pager = {}
        pager['pageSize'] = pageSize
        pager['pageNum'] = pageNum
        l = pager['pageSize']
        o = (pager['pageNum'] - 1) * pager['pageSize']
        count = self.count(table, where)
        pager['pageCount'] = int((count + pager['pageSize'] - 1) / pager['pageSize'])
        if not pager['pageCount']:
            pager['pageCount'] = 1
        dire = ASCENDING
        if direction:
            if direction.lower() == 'desc':
                dire = DESCENDING
        result = self.self_get(table, where).sort(sort, dire).skip(o).limit(l)
        return (result, pager)

    def get_page_tolist(self, table, where, sort, direction, pageSize, pageNum):
        result, pager = self.get_page(table, where, sort, direction, pageSize, pageNum)
        return (list(result), pager)

    def get_one(self, table, where=None):
        tb = self.get_collection(table)
        return tb.find_one(where)

    def insert_one_ret_id(self, table, obj):
        tb = self.get_collection(table)
        return tb.insert(obj)

    def insert_multi_ret_ids(self, table, objs):
        tb = self.get_collection(table)
        return tb.insert(objs)

    def self_delete(self, table, where=None):
        tb = self.get_collection(table)
        return tb.remove(where)

    def delete_all(self, table):
        return self.self_delete(table, where)

    def save_one(self, table, obj):
        tb = self.get_collection(table)
        return tb.update_one({'_id': obj['_id']}, {'$set': obj}, upsert=False)