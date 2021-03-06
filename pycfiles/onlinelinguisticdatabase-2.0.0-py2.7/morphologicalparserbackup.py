# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/onlinelinguisticdatabase/model/morphologicalparserbackup.py
# Compiled at: 2016-09-19 13:27:02
"""Morphological parser backup model"""
from sqlalchemy import Column, Sequence
from sqlalchemy.types import Integer, Unicode, UnicodeText, DateTime, Boolean
from onlinelinguisticdatabase.model.meta import Base, now
import simplejson as json

class MorphologicalParserBackup(Base):
    __tablename__ = 'morphologicalparserbackup'

    def __repr__(self):
        return '<MorphologicalParserBackup (%s)>' % self.id

    id = Column(Integer, Sequence('morphologicalparserbackup_seq_id', optional=True), primary_key=True)
    morphologicalparser_id = Column(Integer)
    UUID = Column(Unicode(36))
    name = Column(Unicode(255))
    description = Column(UnicodeText)
    phonology = Column(UnicodeText)
    morphology = Column(UnicodeText)
    language_model = Column(UnicodeText)
    enterer = Column(UnicodeText)
    modifier = Column(UnicodeText)
    datetime_entered = Column(DateTime)
    datetime_modified = Column(DateTime, default=now)
    compile_succeeded = Column(Boolean, default=False)
    compile_message = Column(Unicode(255))
    compile_attempt = Column(Unicode(36))

    def vivify(self, morphological_parser_dict):
        """The vivify method gives life to a morphology_backup by specifying its
        attributes using the to-be-backed-up morphology (morphological_parser_dict) and the
        modifier (current user).  The relational attributes of the
        to-be-backed-up morphology are converted into (truncated) JSON objects.

        """
        self.UUID = morphological_parser_dict['UUID']
        self.morphologicalparser_id = morphological_parser_dict['id']
        self.name = morphological_parser_dict['name']
        self.description = morphological_parser_dict['description']
        self.phonology = unicode(json.dumps(morphological_parser_dict['phonology']))
        self.morphology = unicode(json.dumps(morphological_parser_dict['morphology']))
        self.language_model = unicode(json.dumps(morphological_parser_dict['language_model']))
        self.enterer = unicode(json.dumps(morphological_parser_dict['enterer']))
        self.modifier = unicode(json.dumps(morphological_parser_dict['modifier']))
        self.datetime_entered = morphological_parser_dict['datetime_entered']
        self.datetime_modified = morphological_parser_dict['datetime_modified']
        self.compile_succeeded = morphological_parser_dict['compile_succeeded']
        self.compile_message = morphological_parser_dict['compile_message']
        self.compile_attempt = morphological_parser_dict['compile_attempt']

    def get_dict(self):
        return {'id': self.id, 
           'morphologicalparser_id': self.morphologicalparser_id, 
           'UUID': self.UUID, 
           'name': self.name, 
           'phonology': self.get_mini_dict_for(self.phonology), 
           'morphology': self.get_mini_dict_for(self.morphology), 
           'language_model': self.get_mini_dict_for(self.language_model), 
           'description': self.description, 
           'enterer': self.get_mini_user_dict(self.enterer), 
           'modifier': self.get_mini_user_dict(self.modifier), 
           'datetime_entered': self.datetime_entered, 
           'datetime_modified': self.datetime_modified, 
           'compile_succeeded': self.compile_succeeded, 
           'compile_message': self.compile_message, 
           'compile_attempt': self.compile_attempt}