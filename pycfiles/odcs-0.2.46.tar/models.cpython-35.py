# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hanzz/releases/odcs/server/odcs/server/models.py
# Compiled at: 2017-09-21 02:38:08
# Size of source mod 2**32: 9689 bytes
""" SQLAlchemy Database models for the Flask app
"""
import os
from datetime import datetime, timedelta
from flask_login import UserMixin
from sqlalchemy.orm import validates
from sqlalchemy.schema import Index
from odcs.server import conf
from odcs.server import db
from odcs.server.events import cache_composes_if_state_changed
from odcs.server.events import start_to_publish_messages
from odcs.server.types import COMPOSE_STATES, INVERSE_COMPOSE_STATES, COMPOSE_FLAGS
from sqlalchemy import event, or_
from flask.ext.sqlalchemy import SignallingSession
event.listen(SignallingSession, 'before_commit', cache_composes_if_state_changed)
event.listen(SignallingSession, 'after_commit', start_to_publish_messages)

def commit_on_success(func):

    def _decorator(*args, **kwargs):
        try:
            try:
                return func(*args, **kwargs)
            except:
                db.session.rollback()
                raise

        finally:
            db.session.commit()

    return _decorator


class ODCSBase(db.Model):
    __abstract__ = True


class User(ODCSBase, UserMixin):
    __doc__ = 'User information table'
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False, unique=True)

    @classmethod
    def find_user_by_name(cls, username):
        """Find a user by username

        :param str username: a string of username to find user
        :return: user object if found, otherwise None is returned.
        :rtype: User
        """
        try:
            return db.session.query(cls).filter(cls.username == username)[0]
        except IndexError:
            return

    @classmethod
    def create_user(cls, username):
        user = cls(username=username)
        db.session.add(user)
        return user


class Compose(ODCSBase):
    __tablename__ = 'composes'
    id = db.Column(db.Integer, primary_key=True)
    owner = db.Column(db.String, nullable=False)
    source_type = db.Column(db.Integer, nullable=False)
    source = db.Column(db.String, nullable=False)
    koji_event = db.Column(db.Integer)
    state = db.Column(db.Integer, nullable=False, index=True)
    results = db.Column(db.Integer, nullable=False)
    packages = db.Column(db.String)
    flags = db.Column(db.Integer)
    time_to_expire = db.Column(db.DateTime, nullable=False, index=True)
    time_submitted = db.Column(db.DateTime, nullable=False)
    time_done = db.Column(db.DateTime)
    time_removed = db.Column(db.DateTime)
    reused_id = db.Column(db.Integer, index=True)

    @classmethod
    def create(cls, session, owner, source_type, source, results, seconds_to_live, packages=None, flags=0):
        now = datetime.utcnow()
        compose = cls(owner=owner, source_type=source_type, source=source, state='wait', results=results, time_submitted=now, time_to_expire=now + timedelta(seconds=seconds_to_live), packages=packages, flags=flags)
        session.add(compose)
        return compose

    @classmethod
    def create_copy(cls, session, compose, owner=None, seconds_to_live=None):
        """
        Creates new compose with all the options influencing the resulting
        compose copied from the `compose`. The `owner` and `seconds_to_live`
        can be set independently. The state of copies compose is "wait".
        """
        now = datetime.utcnow()
        if not seconds_to_live:
            seconds_to_live = conf.seconds_to_live
        compose = cls(owner=owner or compose.owner, source_type=compose.source_type, source=compose.source, state='wait', results=compose.results, time_submitted=now, time_to_expire=now + timedelta(seconds=seconds_to_live), packages=compose.packages, flags=compose.flags, koji_event=compose.koji_event)
        session.add(compose)
        return compose

    @property
    def name(self):
        if self.reused_id:
            return 'odcs-%d' % self.reused_id
        else:
            return 'odcs-%d' % self.id

    @property
    def latest_dir(self):
        return 'latest-%s-1' % self.name

    @property
    def toplevel_dir(self):
        return os.path.join(conf.target_dir, self.latest_dir)

    @property
    def result_repo_dir(self):
        """
        Returns path to compose directory with per-arch repositories with
        results.
        """
        return os.path.join(self.toplevel_dir, 'compose', 'Temporary')

    @property
    def result_repo_url(self):
        """
        Returns public URL to compose directory with per-arch repositories.
        """
        return conf.target_dir_url + '/' + os.path.join(self.latest_dir, 'compose', 'Temporary')

    @property
    def result_repofile_path(self):
        """
        Returns path to .repo file.
        """
        return os.path.join(self.toplevel_dir, 'compose', 'Temporary', self.name + '.repo')

    @property
    def result_repofile_url(self):
        """
        Returns public URL to repofile.
        """
        return conf.target_dir_url + '/' + os.path.join(self.latest_dir, 'compose', 'Temporary', self.name + '.repo')

    @validates('state')
    def validate_state(self, key, field):
        if field in COMPOSE_STATES.values():
            return field
        if field in COMPOSE_STATES:
            return COMPOSE_STATES[field]
        raise ValueError('%s: %s, not in %r' % (key, field, COMPOSE_STATES))

    def json(self):
        flags = []
        for name, value in COMPOSE_FLAGS.items():
            if value == 0:
                pass
            elif self.flags & value:
                flags.append(name)

        return {'id': self.id, 
         'owner': self.owner, 
         'source_type': self.source_type, 
         'source': self.source, 
         'state': self.state, 
         'state_name': INVERSE_COMPOSE_STATES[self.state], 
         'time_to_expire': self._utc_datetime_to_iso(self.time_to_expire), 
         'time_submitted': self._utc_datetime_to_iso(self.time_submitted), 
         'time_done': self._utc_datetime_to_iso(self.time_done), 
         'time_removed': self._utc_datetime_to_iso(self.time_removed), 
         'result_repo': self.result_repo_url, 
         'result_repofile': self.result_repofile_url, 
         'flags': flags}

    @staticmethod
    def _utc_datetime_to_iso(datetime_object):
        """
        Takes a UTC datetime object and returns an ISO formatted string
        :param datetime_object: datetime.datetime
        :return: string with datetime in ISO format
        """
        if datetime_object:
            return datetime_object.strftime('%Y-%m-%dT%H:%M:%SZ')

    @classmethod
    def composes_to_expire(cls):
        now = datetime.utcnow()
        return Compose.query.filter(or_(Compose.state == COMPOSE_STATES['done'], Compose.state == COMPOSE_STATES['failed']), Compose.time_to_expire < now).all()

    def __repr__(self):
        return '<Compose %s, type %r, state %s, owner %s>' % (
         self.source, self.source_type,
         INVERSE_COMPOSE_STATES[self.state], self.owner)

    def get_reused_compose(self):
        """Get compose this compose reuses"""
        return db.session.query(Compose).filter(Compose.id == self.reused_id).first()

    def get_reusing_composes(self):
        """Get composes that are reusing this compose"""
        return db.session.query(Compose).filter(Compose.reused_id == self.id).all()

    def extend_expiration(self, _from, seconds_to_live):
        """Extend time to expire"""
        new_expiration = max(self.time_to_expire, _from + timedelta(seconds=seconds_to_live))
        if new_expiration != self.time_to_expire:
            self.time_to_expire = new_expiration


Index('idx_source_type__state', Compose.source_type, Compose.state)