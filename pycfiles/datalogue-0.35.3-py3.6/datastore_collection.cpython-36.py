# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/datalogue/models/datastore_collection.py
# Compiled at: 2020-05-13 11:17:34
# Size of source mod 2**32: 4219 bytes
from typing import Dict, List, Optional, Union
from datalogue.errors import DtlError
from datalogue.models.datastore import Datastore, _datastore_from_payload
from datalogue.dtl_utils import _parse_list, _parse_uuid
from uuid import UUID

class DatastoreCollection:

    def __init__(self, name: str, store_ids: List[str], stores: Optional[List[Datastore]]=None, description: str=None, tags: List[str]=[], ontology_ids: List[Union[(str, UUID)]]=[], id: Optional[UUID]=None):
        """
        Build a local datastore collection containing a list of datastores for simple viewing and management
        :param name: a name for your datastore collection
        :param store_ids: a list of ids referencing the datastores to be collected in the datastore collection
        :param stores: once created, this property will contain a list of the datastore objects thus collected, for easy iteration
        :param description: a description for your datastore collection,
        :param tags: can be used to apply string tags to your datastore collection
        :param ontology_ids: can be used to map this datastore collection to an ontolog, for the suggestion engine flow accessible on the GUI
        :param id: once creared, this property will contain the unique id
        """
        self.name = name
        self.store_ids = store_ids
        self.stores = stores
        self.id = id
        self.description = description
        self.tags = tags
        self.ontology_ids = ontology_ids
        self._as_payload()

    def __eq__(self, other: 'DatastoreCollection'):
        if isinstance(self, other.__class__):
            return self._as_payload() == other._as_payload()
        else:
            return False

    def __repr__(self):
        return f"{self.__class__.__name__}(id: {self.id}, name: {self.name!r}, description: {self.description!r}, store_ids: {self.store_ids!r}, ontology_ids: {self.ontology_ids!r}, tags: {self.tags!r})"

    def _as_payload(self) -> dict:
        """
        Dictionary representation of the object
        :return:
        """
        base = {'name':self.name, 
         'storeIds':self.store_ids, 
         'description':self.description, 
         'tags':self.tags, 
         'ontologyIds':list(map(lambda u: str(u), self.ontology_ids))}
        if self.id is not None:
            base['id'] = str(self.id)
        return base


def _datastore_collection_from_dict(json: dict) -> Union[(DtlError, DatastoreCollection)]:
    """Datastore Collection instance from dict."""
    name = json.get('name')
    if name is None:
        return DtlError("'name' for a datastore collection should be defined")
    id = json.get('id')
    if id is None:
        return DtlError("'id' for a datastore collection should be defined'")
    id = UUID(id)
    tags = json.get('tags')
    if tags is None:
        return DtlError("'tags' for a datastore collection should be defined'")
    else:
        stores = None
        storeIds = None
        if 'stores' in json.keys():
            stores = _parse_list(_datastore_from_payload)(json.get('stores'))
        if 'storeIds' in json.keys():
            storeIds = json.get('storeIds')
        if storeIds is None:
            if stores is not None:
                if len(stores) > 0:
                    storeIds = list(map(lambda datastore: datastore.id, stores))
        description = json.get('description')
        ontology_ids = json.get('ontologyIds')
        datastore_collection = DatastoreCollection(name, storeIds, stores, description, tags, ontology_ids, id)
        return datastore_collection