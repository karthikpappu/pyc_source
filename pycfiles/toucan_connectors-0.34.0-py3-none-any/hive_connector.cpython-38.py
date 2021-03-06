# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/rachelle2/webprojects/toucan-connectors/toucan_connectors/hive/hive_connector.py
# Compiled at: 2020-04-21 04:11:51
# Size of source mod 2**32: 1124 bytes
import pandas as pd
from pyhive import hive
from toucan_connectors.toucan_connector import ToucanConnector, ToucanDataSource

class HiveDataSource(ToucanDataSource):
    database = 'default'
    database: str
    query: str


class HiveConnector(ToucanConnector):
    data_source_model: HiveDataSource
    host: str
    port = 10000
    port: int
    auth = 'NONE'
    auth: str
    configuration = None
    configuration: dict
    kerberos_service_name = None
    kerberos_service_name: str
    username = None
    username: str
    password = None
    password: str

    def _retrieve_data(self, data_source: HiveDataSource) -> pd.DataFrame:
        cursor = hive.connect(host=(self.host),
          port=(self.port),
          username=(self.username),
          database=(data_source.database),
          auth=(self.auth),
          configuration=(self.configuration),
          kerberos_service_name=(self.kerberos_service_name),
          password=(self.password)).cursor()
        cursor.execute((data_source.query), parameters=(data_source.parameters))
        columns = [metadata[0] for metadata in cursor.description]
        return pd.DataFrame.from_records((cursor.fetchall()), columns=columns)