# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/moretti/PycharmProjects/incubator-superset/superset/migrations/versions/7e3ddad2a00b_results_key_to_query.py
# Compiled at: 2018-08-15 11:21:52
"""results_key to query

Revision ID: 7e3ddad2a00b
Revises: b46fa1b0b39e
Create Date: 2016-10-14 11:17:54.995156

"""
revision = '7e3ddad2a00b'
down_revision = 'b46fa1b0b39e'
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column('query', sa.Column('results_key', sa.String(length=64), nullable=True))


def downgrade():
    op.drop_column('query', 'results_key')