# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/c5756bec8b47_time_grain_sqla.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 2191 bytes
"""Time grain SQLA

Revision ID: c5756bec8b47
Revises: e502db2af7be
Create Date: 2018-06-04 11:12:59.878742

"""
revision = 'c5756bec8b47'
down_revision = 'e502db2af7be'
import json
from alembic import op
from sqlalchemy import Column, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from superset import db
Base = declarative_base()

class Slice(Base):
    __tablename__ = 'slices'
    id = Column(Integer, primary_key=True)
    params = Column(Text)


def upgrade():
    bind = op.get_bind()
    session = db.Session(bind=bind)
    for slc in session.query(Slice).all():
        try:
            params = json.loads(slc.params)
            if params.get('time_grain_sqla') == 'Time Column':
                params['time_grain_sqla'] = None
                slc.params = json.dumps(params, sort_keys=True)
        except Exception:
            pass

    session.commit()
    session.close()


def downgrade():
    bind = op.get_bind()
    session = db.Session(bind=bind)
    for slc in session.query(Slice).all():
        try:
            params = json.loads(slc.params)
            if params.get('time_grain_sqla') is None:
                params['time_grain_sqla'] = 'Time Column'
                slc.params = json.dumps(params, sort_keys=True)
        except Exception:
            pass

    session.commit()
    session.close()