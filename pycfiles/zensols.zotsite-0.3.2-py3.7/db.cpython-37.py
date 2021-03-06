# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/zensols/zotsite/db.py
# Compiled at: 2020-01-03 18:29:22
# Size of source mod 2**32: 8872 bytes
import logging
from pathlib import Path
import sqlite3
from zensols.zotsite.domain import Collection, Library, Item, Note, Name
logger = logging.getLogger(__name__)

class DatabaseReader(object):
    __doc__ = 'Database access to Zotero store.\n\n    '

    def __init__(self, data_dir: Path, name_pat: str='%', library_id: int=1):
        """Initialize

        :param data_dir: directory containing the Zotero DB files (sqlite and
        collections)
        :param name_pat: the SQL pattern to match against subcollection names
        :param library_id: the DB ide of the library to export

        """
        logger.debug(f"data {format(data_dir)}")
        self.data_dir = data_dir
        self.name_pat = name_pat
        self.library_id = library_id

    def _collection_sql(self, whparams):
        """Create an SQL string to get collections rows."""
        return "\nselect c.collectionId c_id, ci.itemId c_iid,\n        c.parentCollectionId c_pid, c.collectionName c_name\n    from collections c\n    left join collectionItems ci on c.collectionId = ci.collectionId\n    where c.libraryId = %(library_id)s and\n          c.collectionName like '%(coll_name)s'\n" % whparams

    def _item_sql(self, whparams):
        """Create an SQL string to get items (attachments) rows."""
        return '\nselect c.collectionId c_id, c.parentCollectionId c_pid,\n           c.collectionName c_name,\n       it.itemId i_id, ia.parentItemId i_pid, it.key, iy.typeName type,\n       ia.contentType content_type, ia.path,\n       itn.title n_title, itn.note n_note, itn.parentItemId n_pid\n  from items it, itemTypes iy\n      left join itemAttachments ia on it.itemId = ia.itemId\n      left join collectionItems ci on ci.itemId = it.itemId\n      left join collections c on c.collectionId = ci.collectionId\n      left join itemNotes itn on it.itemId = itn.itemId\n  where it.itemTypeId = iy.itemTypeId and\n      it.itemId not in (select itemId from deletedItems)\n  order by ci.orderIndex;\n' % whparams

    def _item_meta_sql(self, whparams):
        """Create an SQL string to get items metadata rows."""
        return '\nselect f.fieldName name, iv.value\n  from items i, itemTypes it, itemData id, itemDataValues iv, fields f\n  where i.itemTypeId = it.itemTypeId and\n      i.itemId = id.itemId and\n      id.valueId = iv.valueId and\n      id.fieldId = f.fieldId and\n      i.itemId = %(item_id)s and\n      i.itemId not in (select itemId from deletedItems)' % whparams

    def _item_creators_sql(self, whparams):
        """Return SQL for creators (authors) across several items"""
        return '\nselect c.firstName, c.lastName\n  from itemCreators ic, creators c\n  where ic.creatorID = c.creatorID and\n    ic.itemID = %(item_id)s\n    order by ic.orderIndex' % whparams

    def get_connection(self):
        """Return a database connection the SQLite database.

        """

        def dict_factory(cursor, row):
            d = {}
            for idx, col in enumerate(cursor.description):
                d[col[0]] = row[idx]

            return d

        db_file = Path(self.data_dir, 'zotero.sqlite')
        logger.info(f"reading SQLite file: {db_file}")
        if not db_file.exists():
            raise OSError(f"no such data file: {db_file}")
        conn = sqlite3.connect(db_file)
        conn.row_factory = dict_factory
        return conn

    def _get_item_meta(self, item, conn, whparams):
        """Return the item metadata from the database.

        :param item: the item to fetch data for
        :param conn: the DB connection
        :param whparams: dict of parameters used for the metadata SQL query
        """
        whparams['item_id'] = item['i_id']
        meta = {}
        for row in conn.execute(self._item_meta_sql(whparams)):
            meta[row['name']] = row['value']

        return meta

    def _get_item_creators(self, item, conn, whparams):
        """Return the item metadata from the database.

        :param item: the item to fetch data for
        :param conn: the DB connection
        :param whparams: dict of parameters used for the metadata SQL query
        """
        whparams['item_id'] = item['i_id']
        creators = []
        for row in conn.execute(self._item_creators_sql(whparams)):
            name = Name(row['firstName'], row['lastName'])
            creators.append(name)

        if len(creators) > 0:
            return creators

    def _select_items(self, conn):
        """Return items from the database.

        :param conn: the DB connection
        """
        logger.debug(f"data_dir: {self.data_dir}")
        wparams = {'library_id': self.library_id}
        logger.debug('wparams: %s' % wparams)
        items = {}
        for item in conn.execute(self._item_sql(wparams)):
            item['subs'] = []
            if not item['i_pid']:
                if not item['c_pid']:
                    item['i_pid'] = item['n_pid']
                else:
                    iid = item['i_id']
                    if iid in items:
                        items[iid].append(item)
                items[iid] = [
                 item]

        for itemlst in items.values():
            for item in itemlst:
                meta = self._get_item_meta(item, conn, wparams)
                item['meta'] = meta
                creators = self._get_item_creators(item, conn, wparams)
                item['creators'] = creators

        for itemlst in items.values():
            for item in itemlst:
                i_pid = item['i_pid']
                if i_pid in items:
                    for par in items[i_pid]:
                        par['subs'].append(item)

        flst = []
        for itemlst in items.values():
            flst.extend(itemlst)

        return flst

    def _select_collections(self, conn):
        """Return items from the database.

        :param conn: the DB connection

        """
        logger.debug(f"data_dir: {self.data_dir}")
        wparams = {'library_id':self.library_id,  'coll_name':self.name_pat}
        logger.debug('wparams: %s' % wparams)
        colls = {}
        for row in conn.execute(self._collection_sql(wparams)):
            row['subs'] = []
            colls[row['c_id']] = row

        for coll in colls.values():
            c_pid = coll['c_pid']
            if c_pid not in colls:
                coll['c_pid'] = None
                c_pid = None
            if c_pid:
                par = colls[c_pid]
                par['subs'].append(coll)

        return list(filter(lambda x: x['c_pid'] is None and x['c_id'], colls.values()))

    def _create_item(self, item):
        """Return a domain object that represents an item (i.e. PDF attachement, link,
        note etc).

        """
        children = list(map(lambda x: self._create_item(x), item['subs']))
        if item['type'] == 'note':
            item = Note(item)
        else:
            item = Item(item, children)
        return item

    def _create_collection(self, coll, by_cid):
        """Return a domain object that represents a Zotero DB (sub)collection.

        :param conn: the DB connection
        :param by_cid: parent to child collection IDs

        """
        logger.debug('processing: {} ({}, {})'.format(coll['c_name'], coll['c_id'], coll['c_iid']))
        cid = coll['c_id']
        items = []
        if cid in by_cid:
            toadd = by_cid[cid]
            items.extend(toadd)
            logger.debug('children items: %d' % len(toadd))
        children = list(map(lambda x: self._create_collection(x, by_cid), coll['subs']))
        items = list(map(lambda x: self._create_item(x), items))
        return Collection(coll, items, children)

    def _create_library(self, colls, items):
        """Return a domain object that represents a Zotero DB (sub)collection.

        :param conn: the DB connection
        :param by_cid: parent to child collection IDs

        """
        by_cid = {}
        for i in items:
            cid = i['c_id']
            if cid:
                if cid in by_cid:
                    cid_lst = by_cid[cid]
                else:
                    cid_lst = []
                    by_cid[cid] = cid_lst
                cid_lst.append(i)

        fcolls = []
        for coll in colls:
            fcoll = self._create_collection(coll, by_cid)
            fcolls.append(fcoll)

        lib = Library(self.data_dir, self.library_id, fcolls)
        return lib

    def get_library(self):
        """Get an object graph representing the data in the Zotero database.

        """
        conn = self.get_connection()
        try:
            colls = self._select_collections(conn)
            items = self._select_items(conn)
            lib = self._create_library(colls, items)
        finally:
            conn.close()

        return lib