# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynosql/providers/dynamo.py
# Compiled at: 2019-04-20 13:31:42
from pynosql.providers.base_provider import BaseProvider, UnhandledProviderException, RecordNotFound

class DynamoDBProvider(BaseProvider):
    """ Dynamo DB Provider """

    def __init__(self, aws_client):
        """ Dynamo DB Provider

        :param aws_client: obj AWSClient
        """
        self._aws_client = aws_client

    def get_record(self, model, table, **kwargs):
        """ Get a single record from Dynamo

        :param model: obj BaseModel
        :param table: str table
        :return: dict record
        :raises: ClientException
        """
        table = self._aws_client.client.Table(table)
        response = self._aws_client.call(table.get_item, **kwargs)
        return self._handle_response(model, response, 'Item')

    def get_records(self, model, table, **kwargs):
        """ Get multiple records from DB

        :param model: obj BaseModel
        :param table: str table
        :param options: obj options
        :return: list records
        :raises: ClientException
        """
        table = self._aws_client.client.Table(table)
        response = self._aws_client.call(table.query, **kwargs)
        return self._handle_response(model, response, 'Items', True)

    def scan_records(self, model, table, **kwargs):
        """ Get multiple records from DB through scan without index

        :param model: obj BaseModel
        :param table: str table
        :param options: obj options
        :return: list records
        :raises: ClientException
        """
        table = self._aws_client.client.Table(table)
        response = self._aws_client.call(table.scan, **kwargs)
        return self._handle_response(model, response, 'Items', True)

    def put_record(self, model, table, **kwargs):
        """ Put record into DB

        :param model: obj BaseModel
        :param table: str table
        :return: obj attributes
        :raises: ClientException
        """
        table = self._aws_client.client.Table(table)
        response = self._aws_client.call(table.put_item, **kwargs)
        return self._handle_response(model, response, 'Attributes')

    def delete_record(self, model, table, **kwargs):
        """ Delete record from DB

        :param model: obj BaseModel
        :param table: str table
        :return: obj attributes
        :raises: ClientException
        """
        table = self._aws_client.client.Table(table)
        response = self._aws_client.call(table.delete_item, **kwargs)
        return self._handle_response(model, response, 'Attributes')

    def update_record(self, model, table, data, **kwargs):
        """ Update record in DynamoDB

        :param model: obj model to load record
        :param table: str table
        :param data: obj data to update record
        :return: obj attributes
        :raises: ClientException
        """
        self.get_record(model, table, **kwargs)
        model.load(data)
        self.put_record(model, table, Item=model.model)

    def _handle_response(self, model, data, key=None, is_list=False):
        """ Handle Response of Dynamo Operation

        :param model: obj model
        :param data: obj data
        :param key: str key
        :param is_list: bool if list expected
        :return: obj model
        """
        try:
            if data and key in data:
                if isinstance(data[key], list):
                    return model.load(list(data[key]), is_list)
                else:
                    return model.load(dict(data[key]), is_list)

            elif data and key and key not in data:
                raise RecordNotFound(('Record not found with data: {} and key {}.').format(data, key))
            else:
                if data and not key:
                    return model.load(dict(data), is_list)
                raise RecordNotFound(('Record not found with data: {} and key {}.').format(data, key))
        except RecordNotFound:
            raise
        except Exception as e:
            raise UnhandledProviderException(('UnhandledProviderException: {}').format(str(e.message)))