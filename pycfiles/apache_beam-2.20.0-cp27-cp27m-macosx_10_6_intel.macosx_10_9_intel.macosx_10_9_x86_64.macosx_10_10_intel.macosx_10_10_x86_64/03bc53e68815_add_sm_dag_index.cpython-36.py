# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/migrations/versions/03bc53e68815_add_sm_dag_index.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 1246 bytes
__doc__ = 'merge_heads_2\n\nRevision ID: 03bc53e68815\nRevises: 0a2a5b66e19d, bf00311e1990\nCreate Date: 2018-11-24 20:21:46.605414\n\n'
from alembic import op
revision = '03bc53e68815'
down_revision = ('0a2a5b66e19d', 'bf00311e1990')
branch_labels = None
depends_on = None

def upgrade():
    op.create_index('sm_dag', 'sla_miss', ['dag_id'], unique=False)


def downgrade():
    op.drop_index('sm_dag', table_name='sla_miss')