# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pymysql_sa/base.py
# Compiled at: 2010-12-01 12:24:21
import pymysql
from sqlalchemy import util
from sqlalchemy.dialects.mysql.mysqldb import MySQLDialect_mysqldb

class MySQLDialect_pymysql(MySQLDialect_mysqldb):
    driver = 'pymysql'

    @classmethod
    def dbapi(cls):
        return __import__('pymysql')

    def create_connect_args(self, url):
        opts = url.translate_connect_args(database='db', username='user', password='passwd')
        opts.update(url.query)
        util.coerce_kw_type(opts, 'compress', bool)
        util.coerce_kw_type(opts, 'connect_timeout', int)
        util.coerce_kw_type(opts, 'client_flag', int)
        util.coerce_kw_type(opts, 'local_infile', int)
        util.coerce_kw_type(opts, 'use_unicode', bool)
        util.coerce_kw_type(opts, 'charset', str)
        ssl = {}
        for key in ['ssl_ca', 'ssl_key', 'ssl_cert', 'ssl_capath', 'ssl_cipher']:
            if key in opts:
                ssl[key[4:]] = opts[key]
                util.coerce_kw_type(ssl, key[4:], str)
                del opts[key]

        if ssl:
            opts['ssl'] = ssl
        client_flag = opts.get('client_flag', 0)
        if self.dbapi is not None:
            try:
                from pymysql.constants import CLIENT as CLIENT_FLAGS
                client_flag |= CLIENT_FLAGS.FOUND_ROWS
            except:
                pass
            else:
                opts['client_flag'] = client_flag
        return [[], opts]


dialect = MySQLDialect_pymysql