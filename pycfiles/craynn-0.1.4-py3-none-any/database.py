# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/c24b/projets/crawtext/database/database.py
# Compiled at: 2014-11-06 20:08:33
import pymongo
from pymongo import MongoClient
from pymongo import errors
import re
from datetime import datetime
TASK_MANAGER_NAME = 'crawtext_jobs'
TASK_COLL = 'job'

class Database(object):
    """Database creation"""

    def __init__(self, database_name):
        self.client = MongoClient('mongodb://localhost,localhost:27017')
        self.db_name = database_name
        self.db = getattr(self.client, database_name)

    def set_colls(self):
        self.sources = self.db['sources']
        self.logs = self.db['logs']
        self.results = self.db['results']
        self.queue = self.db['queue']
        return self

    def use_db(self, database_name):
        return self.client[str(database_name)]

    def use_coll(self, coll_name):
        return self.db[coll_name]

    def show_dbs(self):
        return self.client.database_names()

    def create_coll(self, coll_name):
        setattr(self, str(coll_name), self.db[str(coll_name)])
        return self

    def create_colls(self, coll_names=[
 'results', 'sources', 'log', 'queue']):
        for n in coll_names:
            setattr(self, n, self.db[str(n)])

        return [ n for n in self.db.collection_names() ]

    def show_coll(self):
        try:
            print 'using collection %s in DB : %s' % (self.coll_name, self.db_name)
            return self.coll_name
        except AttributeError:
            return False

    def show_coll_items(self, coll_name):
        return [ n for n in self.db[str(coll_name)].find() ]

    def drop(self, type, name):
        if type == 'collection':
            return self.db[str(name)].drop()
        else:
            if type == 'database':
                return self.client.drop_database(str(name))
            print 'Unknown Type'
            return False

    def drop_db(self):
        return self.client.drop_database(str(self.db_name))

    def drop_all_dbs(self):
        """remove EVERY SINGLE MONGO DATABASE"""
        for n in self.show_dbs():
            self.use_db(n)
            self.drop('database', n)

    def insert_log(self, url, log):
        del log['url']
        try:
            del log['html']
        except KeyError:
            pass

        if url not in self.db.sources.distinct('url'):
            exists = self.db.sources.find_one({'url': url})
            if exists is not None:
                self.db.sources.update({'_id': exists['_id']}, {'$push': log})
        elif url not in self.db.logs.distinct('url'):
            self.db.logs.insert({'url': url, 'msg': [log['msg']], 'status': [log['status']], 'code': [log['code']]})
        else:
            exists = self.db.logs.find_one({'url': url})
            if exists is not None:
                try:
                    self.db.logs.update({'_id': exists['_id']}, {'$push': log})
                except Exception as e:
                    self.db.logs.update({'_id': exists['_id']}, {'msg': [log['msg']], 'status': [log['status']], 'code': [log['code']]})

        return

    def insert_result(self, log):
        return self.db.results.insert(log)

    def sources_stats(self):
        self.show_stats()
        return self.template[3]

    def results_stats(self):
        self.show_stats()
        return self.template[1]

    def results_stats(self):
        self.show_stats()
        return self.template[2]

    def show_stats(self):
        """Output the current stats of database in Terminal"""
        self.stats()
        date = datetime.now()
        date = date.strftime('- %d/%M/%Y at %H:%M -')
        title = '==== Project: %s ====\n%s' % (str(self.db_name).capitalize(), date)
        results = '#Results:\n\t-Total:%d\n\t-Unique urls:%d' % (self.results_nb, self.uniq_results_nb)
        errors = '#Errors:\n\t-Total:%d\n\t-Unique:%d' % (self.logs_nb, self.uniq_logs_nb)
        sources = '#Sources:\n\t-Total: %d\n-Unique: %d\n\t-Valid: %d\n\t-Invalid: %d\nCollected methods:\n\t-From search:%d\n\t-From file:%d\n\t-Manual:%d\n\t-Automatic:%d' % (self.sources_nb, self.uniq_sources_nb, self.active_sources_nb, self.inactive_sources_nb, self.bing_sources, self.file_sources, self.manual_sources, self.expanded_sources)
        process = '#Process:\n\t-Total: %d\n\t-Unique: %d\n\t-Treated: %d' % (self.queue_nb, self.uniq_queue_nb, self.treated_nb)
        other = '#Other:\n\tName of the database: %s\n\tSize of the database: %d MB' % (self.db_name, self.db.command('dbStats', 1024)['storageSize'] / 1024 / 1024.0)
        self.template = [title, results, errors, sources, process, other]
        return ('\n').join(self.template)

    def stats(self):
        self.sources_nb = self.db.sources.count()
        self.uniq_sources_nb = len(self.db.sources.distinct('url'))
        self.inactive_sources_nb = self.db.sources.find({'status': False}, {'status': {'$slice': -1}}).count()
        self.active_sources_nb = self.sources_nb - self.inactive_sources_nb
        self.bing_sources = self.db.sources.find({'origin': 'bing'}).count()
        self.file_sources = self.db.sources.find({'origin': 'file'}).count()
        self.manual_sources = self.db.sources.find({'origin': 'manual'}).count()
        self.expanded_sources = self.db.sources.find({'origin': 'automatic'}).count()
        self.results_nb = self.db.results.count()
        self.uniq_results_nb = len(self.db.results.distinct('url'))
        self.logs_nb = self.db.logs.count()
        self.uniq_logs_nb = len(self.db.logs.distinct('url'))
        self.non_pertinent_nb = self.db.logs.find({'code': 800}, {'code': {'$slice': -1}}).count()
        self.treated_nb = int(int(self.db.results.count()) + int(self.db.logs.count()))
        self.queue_nb = self.db.queue.count()
        self.uniq_queue_nb = len(self.db.queue.distinct('url'))
        return self

    def mail_report(self):
        self.show_stats()
        title = 'Report for project %s' % str(self.db_name)
        template = [
         title]
        template.append('<ul>')
        for n in self.template:
            chunk = n.split('\n')
            for c in chunk:
                if c.startswith('#'):
                    c = '<h3>%s</h3>' % str(c)
                elif c.startswith('='):
                    c = '<h2>%s</h2>' % str(c)
                else:
                    c = '<li>%s</li>' % str(c)
                template.append(c)

        template.append('</ul>')
        return ('').join(template)


class TaskDB(Database):

    def __init__(self):
        Database.__init__(self, TASK_MANAGER_NAME)
        self.coll = self.db[str(TASK_COLL)]

    def get(self):
        return self.coll


if __name__ == '__main':
    print 'Database'