# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pgobserver_gatherer/gatherer_statements.py
# Compiled at: 2016-04-20 09:16:45
# Size of source mod 2**32: 4438 bytes
import re
from pgobserver_gatherer.gatherer_base import GathererBase
import pgobserver_gatherer.datadb as datadb
from pgobserver_gatherer.globalconfig import Datasets
from pgobserver_gatherer.globalconfig import SUPPORTED_DATASETS
ROW_LIMITS_FOR_SINGLE_ORDERING_CRITERIONS = 500
QUERY_TRANSFORMATION_REGEXES = [{'pattern': re.compile('[\\t\\s]+'),  'replace': ' '}, {'pattern': re.compile('/\\*(.*?)\\*/'),  'replace': ''}]

class StatStatementsGatherer(GathererBase):

    def __init__(self, host_data, settings):
        GathererBase.__init__(self, host_data, settings, Datasets.STATEMENTS)
        self.interval_seconds = settings[SUPPORTED_DATASETS[Datasets.STATEMENTS][0]] * 60
        self.columns_to_store = ['ssd_host_id', 'ssd_timestamp', 'ssd_query', 'ssd_query_id', 'ssd_calls', 'ssd_total_time',
         'ssd_blks_read', 'ssd_blks_written', 'ssd_temp_blks_read', 'ssd_temp_blks_written']
        self.datastore_table_name = 'monitor_data.stat_statements_data'

    def gather_data(self):
        sql_get = "\n        with q_data as (\n          select\n            now() as ssd_timestamp,\n            ltrim(regexp_replace(query, E'[ \\t\\n\\r]+' , ' ', 'g')) as ssd_query,\n            sum(s.calls)::int8 as ssd_calls,\n            round(sum(s.total_time))::int8 as ssd_total_time,\n            sum(shared_blks_read+local_blks_read)::int8 as ssd_blks_read,\n            sum(shared_blks_written+local_blks_written)::int8 as ssd_blks_written,\n            sum(temp_blks_read)::int8 as ssd_temp_blks_read,\n            sum(temp_blks_written)::int8 as ssd_temp_blks_written\n          from\n            zz_utils.get_stat_statements() s\n          where\n            calls > 1\n            and total_time > 0\n            and not upper(s.query) like any (array['DEALLOCATE%', 'SET %', 'RESET %', 'BEGIN%', 'BEGIN;',\n              'COMMIT%', 'END%', 'ROLLBACK%', 'SHOW%', '<INSUFFICIENT PRIVILEGE>'])\n          group by\n            query\n        )\n        select * from (\n          select\n            *\n          from\n            q_data\n          where\n            ssd_total_time > 0\n          order by\n            ssd_total_time desc\n          limit {row_limit}\n        ) a\n        union\n        select * from (\n          select\n            *\n          from\n            q_data\n          order by\n            ssd_calls desc\n          limit {row_limit}\n        ) a\n        union\n        select * from (\n          select\n            *\n          from\n            q_data\n          where\n            ssd_blks_read > 0\n          order by\n            ssd_blks_read desc\n          limit {row_limit}\n        ) a\n        union\n        select * from (\n          select\n            *\n          from\n            q_data\n          where\n            ssd_blks_written > 0\n          order by\n            ssd_blks_written desc\n          limit {row_limit}\n        ) a\n        union\n        select * from (\n          select\n            *\n          from\n            q_data\n          where\n            ssd_temp_blks_read > 0\n          order by\n            ssd_temp_blks_read desc\n          limit {row_limit}\n        ) a\n        union\n        select * from (\n          select\n            *\n          from\n            q_data\n          where\n            ssd_temp_blks_written > 0\n          order by\n            ssd_temp_blks_written desc\n          limit {row_limit}\n        ) a\n".format(row_limit=ROW_LIMITS_FOR_SINGLE_ORDERING_CRITERIONS)
        data = datadb.executeOnHost(self.host_data['host_name'], self.host_data['host_port'], self.host_data['host_db'], self.host_data['host_user'], self.host_data['host_password'], sql_get)
        for d in data:
            d['ssd_host_id'] = self.host_id
            d['ssd_query'] = StatStatementsGatherer.perform_regex_transformations(d['ssd_query'])
            if 'ssd_query_id' not in d:
                d['ssd_query_id'] = d['ssd_query'].__hash__()
                continue

        return data

    @staticmethod
    def perform_regex_transformations(some_string):
        ret_string = some_string
        for tf_rule in QUERY_TRANSFORMATION_REGEXES:
            ret_string = tf_rule['pattern'].sub(tf_rule['replace'], ret_string)

        return ret_string


if __name__ == '__main__':
    print(StatStatementsGatherer.perform_regex_transformations('a/*\t\nb*/c'))