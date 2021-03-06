# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kalimaha/Development/git-repositories/Geobricks/pgeo/pgeo/db/mongo/metadata/db.py
# Compiled at: 2014-08-08 09:13:30
import pymongo
from pgeo.db.mongo import common
from pgeo.config.settings import settings
from pgeo.config.settings import read_config_file_json
client = pymongo.MongoClient(settings['db']['metadata']['connection'])
database = settings['db']['metadata']['database']
document_layer = settings['db']['metadata']['document']['layer']

def insert_metadata(json):
    """
    Insert Layer Metadata in mongodb
    @param json: json data
    @return: id
    """
    return common.insert(client, database, document_layer, json)


def remove_metadata(json):
    """
    Delete Layer Metadata in mongodb
    @param json: json data
    @return: id
    """
    return common.remove(client, database, document_layer, json)


def remove_metadata_by_id(id):
    """
    Delete Layer Metadata in mongodb
    @param id: Metadata's id
    @return: id
    """
    return common.remove_by_id(client, database, document_layer, id)


def find(collection):
    """
    Return entire collection
    @param collection: collection
    @return: collection
    """
    return common.find(client, database, collection, {'$query': {}, '$orderby': [{'layertitle': 1}, {'date': 1}]})


def find_query(collection, query):
    """
    Return entire collection
    @param collection: collection
    @param query: mongodb query
    @return: collection
    """
    return common.find(client, database, collection, query)


def find_by_layer_name(collection, layer_name):
    """
    Return the document containing the layername
    @param collection: collection (i.e. layer)
    @param layer_name: layername stored in the db
    @return: collection
    """
    return common.find(client, database, collection, {'$query': {'layername': layer_name}, '$orderby': [{'layertitle': 1}]})


def find_by_code(collection, code, sort_date):
    return common.find(client, database, collection, {'$query': {'code': code}, '$orderby': [{'coverageTime.from': sort_date}]})