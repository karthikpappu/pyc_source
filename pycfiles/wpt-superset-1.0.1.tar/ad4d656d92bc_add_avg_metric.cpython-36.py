# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/leonardo/proyectos/dashboard/incubator-superset/superset/migrations/versions/ad4d656d92bc_add_avg_metric.py
# Compiled at: 2019-01-19 16:19:59
# Size of source mod 2**32: 1425 bytes
"""Add avg() to default metrics

Revision ID: ad4d656d92bc
Revises: b46fa1b0b39e
Create Date: 2016-10-25 10:16:39.871078

"""
revision = 'ad4d656d92bc'
down_revision = '7e3ddad2a00b'
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column('columns', sa.Column('avg', (sa.Boolean()), nullable=True))
    op.add_column('table_columns', sa.Column('avg', (sa.Boolean()), nullable=True))


def downgrade():
    with op.batch_alter_table('columns') as (batch_op):
        batch_op.drop_column('avg')
    with op.batch_alter_table('table_columns') as (batch_op):
        batch_op.drop_column('avg')