# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Projects\usersapi\midaxusersutils\migrations\versions\9a8c2fa38f9f_.py
# Compiled at: 2018-11-01 11:28:27
# Size of source mod 2**32: 3609 bytes
"""empty message

Revision ID: 9a8c2fa38f9f
Revises: 
Create Date: 2018-11-01 17:28:27.320909

"""
from alembic import op
import sqlalchemy as sa, midaxusers.migration_types
revision = '9a8c2fa38f9f'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('USERS', sa.Column('id', (sa.Integer()), nullable=False), sa.Column('uuid', (midaxusers.migration_types.HybridUniqueIdentifier()), nullable=False), sa.Column('domain', sa.String(length=64), nullable=True), sa.Column('role', (sa.Integer()), nullable=True), sa.Column('active', sa.Boolean(name='bl_U_active'), server_default=(sa.text('1')), nullable=True), sa.Column('first_name', sa.String(length=64), nullable=True), sa.Column('middle_name', sa.String(length=64), nullable=True), sa.Column('last_name', sa.String(length=64), nullable=True), sa.Column('phone', sa.String(length=64), nullable=True), sa.Column('position', sa.String(length=20), nullable=True), sa.Column('time_updated', sa.DateTime(timezone=True), server_default=(sa.text('CURRENT_TIMESTAMP')), nullable=True), sa.PrimaryKeyConstraint('id', name=(op.f('pk_USERS'))), sa.UniqueConstraint('uuid', name='user_uuid_uq'))
    op.create_index((op.f('ix_USERS_domain')), 'USERS', ['domain'], unique=False)
    op.create_table('USER_ATTRIBUTES', sa.Column('user_uuid', (midaxusers.migration_types.HybridUniqueIdentifier()), nullable=False), sa.Column('name', sa.String(length=64), nullable=False), sa.Column('value', sa.String(length=64), nullable=True), sa.Column('time_updated', sa.DateTime(timezone=True), server_default=(sa.text('CURRENT_TIMESTAMP')), nullable=True), sa.ForeignKeyConstraint(['user_uuid'], ['USERS.uuid'], name=(op.f('fk_USER_ATTRIBUTES_user_uuid_U')), onupdate='CASCADE', ondelete='CASCADE'), sa.PrimaryKeyConstraint('user_uuid', 'name', name='userattributes_pk'))
    op.create_index((op.f('ix_USER_ATTRIBUTES_user_uuid')), 'USER_ATTRIBUTES', ['user_uuid'], unique=False)
    op.create_table('USER_LOGINS', sa.Column('id', (sa.Integer()), nullable=False), sa.Column('user_uuid', (midaxusers.migration_types.HybridUniqueIdentifier()), nullable=False), sa.Column('login_type', sa.String(length=40), nullable=False), sa.Column('login_key', sa.String(length=120), nullable=False), sa.Column('password_hash', sa.String(length=256), nullable=False), sa.Column('force_password_change', sa.Boolean(name='bl_UL_fpc'), server_default=(sa.text('0')), nullable=True), sa.Column('time_updated', sa.DateTime(timezone=True), server_default=(sa.text('CURRENT_TIMESTAMP')), nullable=True), sa.ForeignKeyConstraint(['user_uuid'], ['USERS.uuid'], name=(op.f('fk_USER_LOGINS_user_uuid_U')), onupdate='CASCADE', ondelete='CASCADE'), sa.PrimaryKeyConstraint('id', name=(op.f('pk_USER_LOGINS'))), sa.UniqueConstraint('login_type', 'login_key', name='login_user_uq'))
    op.create_index((op.f('ix_USER_LOGINS_user_uuid')), 'USER_LOGINS', ['user_uuid'], unique=False)


def downgrade():
    op.drop_index((op.f('ix_USER_LOGINS_user_uuid')), table_name='USER_LOGINS')
    op.drop_table('USER_LOGINS')
    op.drop_index((op.f('ix_USER_ATTRIBUTES_user_uuid')), table_name='USER_ATTRIBUTES')
    op.drop_table('USER_ATTRIBUTES')
    op.drop_index((op.f('ix_USERS_domain')), table_name='USERS')
    op.drop_table('USERS')