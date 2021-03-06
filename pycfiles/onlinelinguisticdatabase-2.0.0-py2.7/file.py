# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/onlinelinguisticdatabase/model/file.py
# Compiled at: 2016-09-19 13:27:02
"""File model"""
from sqlalchemy import Column, Sequence, ForeignKey
from sqlalchemy.types import Integer, Unicode, UnicodeText, Date, DateTime, Float
from sqlalchemy.orm import relation
from onlinelinguisticdatabase.model.meta import Base, now
import logging
log = logging.getLogger(__name__)

class FileTag(Base):
    __tablename__ = 'filetag'
    id = Column(Integer, Sequence('filetag_seq_id', optional=True), primary_key=True)
    file_id = Column(Integer, ForeignKey('file.id'))
    tag_id = Column(Integer, ForeignKey('tag.id'))
    datetime_modified = Column(DateTime(), default=now)


class File(Base):
    """There are 3 types of file:
    
    1. Standard files: their content is a file in /files/filename.  These files
       have a filename attribute.
    2. Subinterval-referring A/V files: these refer to another OLD file for
       their content.  These files have a parent_file attribute (as well as start
       and end attributes.)
    3. Externally hosted files: these refer to a file hosted on another server.
       They have a url attribute (and optionally a password attribute as well.)
    """
    __tablename__ = 'file'

    def __repr__(self):
        return '<File (%s)>' % self.id

    id = Column(Integer, Sequence('file_seq_id', optional=True), primary_key=True)
    filename = Column(Unicode(255), unique=True)
    name = Column(Unicode(255))
    MIME_type = Column(Unicode(255))
    size = Column(Integer)
    description = Column(UnicodeText)
    date_elicited = Column(Date)
    datetime_entered = Column(DateTime)
    datetime_modified = Column(DateTime, default=now)
    enterer_id = Column(Integer, ForeignKey('user.id', ondelete='SET NULL'))
    enterer = relation('User', primaryjoin='File.enterer_id==User.id')
    elicitor_id = Column(Integer, ForeignKey('user.id', ondelete='SET NULL'))
    elicitor = relation('User', primaryjoin='File.elicitor_id==User.id')
    speaker_id = Column(Integer, ForeignKey('speaker.id', ondelete='SET NULL'))
    speaker = relation('Speaker')
    utterance_type = Column(Unicode(255))
    tags = relation('Tag', secondary=FileTag.__table__, backref='files')
    url = Column(Unicode(255))
    password = Column(Unicode(255))
    parent_file_id = Column(Integer, ForeignKey('file.id', ondelete='SET NULL'))
    parent_file = relation('File', remote_side=[id])
    start = Column(Float)
    end = Column(Float)
    lossy_filename = Column(Unicode(255))

    def get_dict(self):
        """Return a Python dictionary representation of the File.  This
        facilitates JSON-stringification, cf. utils.JSONOLDEncoder.  Relational
        data are truncated.
        """
        return {'id': self.id, 
           'date_elicited': self.date_elicited, 
           'datetime_entered': self.datetime_entered, 
           'datetime_modified': self.datetime_modified, 
           'filename': self.filename, 
           'name': self.name, 
           'lossy_filename': self.lossy_filename, 
           'MIME_type': self.MIME_type, 
           'size': self.size, 
           'description': self.description, 
           'utterance_type': self.utterance_type, 
           'url': self.url, 
           'password': self.password, 
           'enterer': self.get_mini_user_dict(self.enterer), 
           'elicitor': self.get_mini_user_dict(self.elicitor), 
           'speaker': self.get_mini_speaker_dict(self.speaker), 
           'tags': self.get_tags_list(self.tags), 
           'forms': self.get_forms_list(self.forms), 
           'parent_file': self.get_mini_file_dict(self.parent_file), 
           'start': self.start, 
           'end': self.end}