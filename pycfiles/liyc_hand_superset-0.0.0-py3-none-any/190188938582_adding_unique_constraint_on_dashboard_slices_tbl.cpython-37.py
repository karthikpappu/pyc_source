# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: f:\pythonfile\hand_superset\superset\migrations\versions\190188938582_adding_unique_constraint_on_dashboard_slices_tbl.py
# Compiled at: 2019-08-01 07:27:28
# Size of source mod 2**32: 3162 bytes
"""Remove duplicated entries in dashboard_slices table and add unique constraint

Revision ID: 190188938582
Revises: d6ffdf31bdd4
Create Date: 2019-07-15 12:00:32.267507

"""
import logging
from alembic import op
from sqlalchemy import and_, Column, ForeignKey, Integer, Table
from sqlalchemy.ext.declarative import declarative_base
from superset import db
revision = '190188938582'
down_revision = 'd6ffdf31bdd4'
Base = declarative_base()

class DashboardSlices(Base):
    __tablename__ = 'dashboard_slices'
    id = Column(Integer, primary_key=True)
    dashboard_id = Column(Integer, ForeignKey('dashboards.id'))
    slice_id = Column(Integer, ForeignKey('slices.id'))


def upgrade():
    bind = op.get_bind()
    session = db.Session(bind=bind)
    dup_records = session.query(DashboardSlices.dashboard_id, DashboardSlices.slice_id, db.func.count(DashboardSlices.id)).group_by(DashboardSlices.dashboard_id, DashboardSlices.slice_id).having(db.func.count(DashboardSlices.id) > 1).all()
    for record in dup_records:
        print('remove duplicates from dashboard {} slice {}'.format(record.dashboard_id, record.slice_id))
        ids = [item.id for item in session.query(DashboardSlices.id).filter(and_(DashboardSlices.slice_id == record.slice_id, DashboardSlices.dashboard_id == record.dashboard_id)).offset(1)]
        session.query(DashboardSlices).filter(DashboardSlices.id.in_(ids)).delete(synchronize_session=False)

    try:
        with op.batch_alter_table('dashboard_slices') as (batch_op):
            batch_op.create_unique_constraint('uq_dashboard_slice', ['dashboard_id', 'slice_id'])
    except Exception as e:
        try:
            logging.exception(e)
        finally:
            e = None
            del e


def downgrade():
    try:
        with op.batch_alter_table('dashboard_slices') as (batch_op):
            batch_op.drop_constraint('uq_dashboard_slice', type_='unique')
    except Exception as e:
        try:
            logging.exception(e)
        finally:
            e = None
            del e