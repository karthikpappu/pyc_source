# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/FeatureServer/DataSource/SQLite.py
# Compiled at: 2008-03-28 21:34:04
__author__ = 'MetaCarta'
__copyright__ = 'Copyright (c) 2006-2008 MetaCarta'
__license__ = 'Clear BSD'
__version__ = '$Id: SQLite.py 449 2008-03-29 01:34:04Z brentp $'
import re, copy
from FeatureServer.DataSource import DataSource
from FeatureServer.Feature import Feature
import sys
try:
    import sqlite3
except:
    from pysqlite2 import dbapi2 as sqlite3

class SQLite(DataSource):
    """Similar to the PostGIS datasource. Works with the 
       built in sqlite in Python2.5+, or with pysqlite2."""
    __module__ = __name__
    wkt_linestring_match = re.compile('\\(([^()]+)\\)')

    def __init__(self, name, srid=4326, order=None, writable=True, **args):
        DataSource.__init__(self, name, **args)
        self.table = args.get('layer') or name
        self.fid_col = 'feature_id'
        self.geom_col = 'wkt_geometry'
        self.order = order
        self.srid = srid
        self.db = None
        self.dsn = args.get('dsn') or args.get('file')
        self.writable = writable
        return

    def begin(self):
        self.db = sqlite3.connect(self.dsn)
        self.db.row_factory = sqlite3.Row
        if self.table not in self.tables():
            c = self.db.cursor()
            c.executescript(self.schema())

    def tables(self):
        c = self.db.cursor()
        res = c.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
        return [ r[0] for r in res ]

    def schema(self):
        return "CREATE TABLE '%s' (\n    feature_id   INTEGER PRIMARY KEY,\n    xmin INTEGER,\n    ymin INTEGER,\n    xmax INTEGER,\n    ymax INTEGER,\n    date_created DATETIME,\n    date_modified DATETIME,\n    %s VARCHAR\n);\nCREATE TABLE '%s_attrs' (\n    id     INTEGER PRIMARY KEY,\n    feature_id  INTEGER,\n    title  VARCHAR(256),\n    key    VARCHAR(256),\n    value TEXT\n);    \nCREATE INDEX %s_xy_idx ON %s (xmin, xmax, ymin, ymax);\nCREATE INDEX %s_attrs_title_idx on %s_attrs (title);\nCREATE INDEX %s_attrs_feature_id on %s_attrs (feature_id);\nCREATE INDEX %s_attrs_%s_key on %s_attrs (key);\n\n/* automatic timestamp, but dont override if one is sent in */\nCREATE TRIGGER %s_insert_date_trigger \nAFTER INSERT ON %s\nBEGIN\n        UPDATE %s SET date_created = datetime('now', 'localtime')\n                WHERE feature_id = NEW.feature_id AND\n                NEW.date_created IS NULL;\n        UPDATE %s SET date_modified = datetime('now', 'localtime')\n                WHERE feature_id = NEW.feature_id;\nEND; \nCREATE TRIGGER %s_update_date_trigger \n/* update the main table when attrs are modified */\nAFTER UPDATE ON %s_attrs\nBEGIN\n        UPDATE %s SET date_modified = datetime('now', 'localtime')\n                WHERE feature_id = NEW.feature_id;\nEND; \n\n" % tuple([self.table, self.geom_col] + list((self.table,) * 17))

    def commit(self):
        if self.writable:
            self.db.commit()
        self.db.close()

    def rollback(self):
        if self.writable:
            self.db.rollback()
        self.db.close()

    def column_names(self, feature):
        return feature.properties.keys()

    def value_formats(self, feature):
        values = []
        for (key, val) in feature.properties.items():
            values.append(':%s' % key)

        return values

    def feature_predicates(self, feature):
        columns = self.column_names(feature)
        values = self.value_formats(feature)
        predicates = []
        for pair in zip(columns, values):
            if pair[0] != self.geom_col:
                predicates.append(' %s = %s' % pair)
            else:
                predicates.append(' %s = %s ' % (self.geom_col, self.to_wkt(feature.geometry)))

        return predicates

    def feature_values(self, feature):
        return copy.deepcopy(feature.properties)

    def to_wkt(self, geom):

        def coords_to_wkt(coords):
            return (',').join([ '%f %f' % tuple(c) for c in coords ])

        coords = geom['coordinates']
        if geom['type'] == 'Point':
            return 'POINT(%s)' % coords_to_wkt(coords)
        elif geom['type'] == 'Line':
            return 'LINESTRING(%s)' % coords_to_wkt(coords)
        elif geom['type'] == 'Polygon':
            rings = [ '(' + coords_to_wkt(ring) + ')' for ring in coords ]
            rings = (',').join(rings)
            return 'POLYGON(%s)' % rings
        else:
            raise Exception("Couldn't create WKT from geometry of type %s (%s). Only Point, Line, Polygon are supported." % (geom['type'], geom))

    def from_wkt(self, geom):
        coords = []
        for line in self.wkt_linestring_match.findall(geom):
            ring = []
            for pair in line.split(','):
                ring.append(map(float, pair.split(' ')))

            coords.append(ring)

        if geom.startswith('POINT'):
            geomtype = 'Point'
            coords = coords[0]
        elif geom.startswith('LINESTRING'):
            geomtype = 'Line'
            coords = coords[0]
        elif geom.startswith('POLYGON'):
            geomtype = 'Polygon'
        else:
            geomtype = geom[:geom.index['(']]
            raise Error('Unsupported geometry type %s' % geomtype)
        return {'type': geomtype, 'coordinates': coords}

    def create(self, action):
        feature = action.feature
        bbox = feature.get_bbox()
        columns = (', ').join([self.geom_col, 'xmin,ymin,xmax,ymax'])
        values = [self.to_wkt(feature.geometry)] + list(bbox)
        sql = 'INSERT INTO "%s" (%s) VALUES (?,?,?,?,?)' % (self.table, columns)
        cursor = self.db.cursor()
        res = cursor.execute(str(sql), values)
        action.id = res.lastrowid
        insert_tuples = [ (res.lastrowid, k, v) for (k, v) in feature.properties.items() if k != 'title' ]
        if 'title' in feature.properties:
            insert_tuples.append((res.lastrowid, 'title', feature.properties['title']))
        sql = 'INSERT INTO "%s_attrs" (feature_id, key, value) VALUES (?, ?, ?)' % (self.table,)
        cursor.executemany(sql, insert_tuples)
        self.db.commit()
        return self.select(action)

    def update(self, action):
        feature = action.feature
        bbox = feature.get_bbox()
        predicates = self.feature_predicates(feature)
        sql = 'UPDATE "%s_attrs" SET value = :value WHERE key = :key AND %s = %d' % (self.table, self.fid_col, action.id)
        cursor = self.db.cursor()
        predicate_list = []
        for i in range(0, len(predicates) - 1, 2):
            predicate_list.append(dict(key=predicates[i], value=predicates[(i + 1)]))

        cursor.executemany(str(sql), predicate_list)
        geom_sql = 'UPDATE %s SET %s = ?, xmin = ?, ymin = ?, xmax = ?, ymax = ? WHERE %s = %d' % (self.table, self.geom_col, self.fid_col, action.id)
        cursor.execute(geom_sql, [self.to_wkt(feature.geometry)] + list(bbox))
        self.db.commit()
        return self.select(action)

    def delete(self, action):
        sql = 'DELETE FROM "%s" WHERE %s = :%s' % (self.table, self.fid_col, self.fid_col)
        cursor = self.db.cursor()
        cursor.execute(str(sql), {self.fid_col: action.id})
        sql = 'DELETE FROM "%s_attrs" WHERE %s = :%s' % (self.table, self.fid_col, self.fid_col)
        cursor.execute(str(sql), {self.fid_col: action.id})
        self.db.commit()
        return []

    def select(self, action):
        cursor = self.db.cursor()
        features = []
        sql_attrs = 'SELECT key, value FROM "%s_attrs" WHERE feature_id = :feature_id' % (self.table,)
        selection_dict = {}
        if action.id is not None:
            sql = 'SELECT * FROM "%s" WHERE %s = ?' % (self.table, self.fid_col)
            cursor.execute(str(sql), (action.id,))
            results = [cursor.fetchone()]
        else:
            match = Feature(props=action.attributes)
            filters = match.properties.items()
            sql = 'SELECT DISTINCT(t.feature_id), t.%s, t.%s FROM "%s" t, "%s_attrs" a WHERE a.feature_id = t.feature_id ' % (self.geom_col, self.fid_col, self.table, self.table)
            select_dict = {}
            if filters:
                for (ii, filter) in enumerate(filters):
                    select_dict['key%i' % ii] = filter[0]
                    select_dict['value%i' % ii] = filter[1]
                    sql += ' AND a.key = :key%i AND a.value = :value%i' % (ii, ii)

            bbox = ''
            if action.bbox:
                bbox = ' AND %f   > t.xmin                      AND t.xmax > %f                      AND %f   > t.ymin                      AND t.ymax >  %f ' % (action.bbox[2], action.bbox[0], action.bbox[3], action.bbox[1])
            sql += bbox
            sql += self.order or ''
            sql += ' LIMIT %d' % (action.maxfeatures or 1000,)
            if action.startfeature:
                sql += ' OFFSET %d' % action.startfeature
            cursor.execute(str(sql), select_dict)
            results = cursor.fetchall()
        for row in results:
            attrs = cursor.execute(sql_attrs, dict(feature_id=row['feature_id'])).fetchall()
            if attrs == []:
                continue
            d = {}
            for attr in attrs:
                d[attr[0]] = attr[1]

            geom = self.from_wkt(row[self.geom_col])
            id = row[self.fid_col]
            if geom:
                features.append(Feature(id, geom, d))

        return features