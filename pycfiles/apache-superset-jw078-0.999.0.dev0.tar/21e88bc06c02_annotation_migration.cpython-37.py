# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/21e88bc06c02_annotation_migration.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 2915 bytes
import json
from alembic import op
from sqlalchemy import Column, Integer, or_, String, Text
from sqlalchemy.ext.declarative import declarative_base
from superset import db
revision = '21e88bc06c02'
down_revision = '67a6ac9b727b'
Base = declarative_base()

class Slice(Base):
    __tablename__ = 'slices'
    id = Column(Integer, primary_key=True)
    viz_type = Column(String(250))
    params = Column(Text)


def upgrade():
    bind = op.get_bind()
    session = db.Session(bind=bind)
    for slc in session.query(Slice).filter(or_(Slice.viz_type.like('line'), Slice.viz_type.like('bar'))):
        params = json.loads(slc.params)
        layers = params.get('annotation_layers', [])
        if layers:
            new_layers = []
            for layer in layers:
                new_layers.append({'annotationType':'INTERVAL', 
                 'style':'solid', 
                 'name':'Layer {}'.format(layer), 
                 'show':True, 
                 'overrides':{'since':None, 
                  'until':None}, 
                 'value':layer, 
                 'width':1, 
                 'sourceType':'NATIVE'})

            params['annotation_layers'] = new_layers
            slc.params = json.dumps(params)
            session.merge(slc)
            session.commit()

    session.close()


def downgrade():
    bind = op.get_bind()
    session = db.Session(bind=bind)
    for slc in session.query(Slice).filter(or_(Slice.viz_type.like('line'), Slice.viz_type.like('bar'))):
        params = json.loads(slc.params)
        layers = params.get('annotation_layers', [])
        if layers:
            params['annotation_layers'] = [layer['value'] for layer in layers]
            slc.params = json.dumps(params)
            session.merge(slc)
            session.commit()

    session.close()