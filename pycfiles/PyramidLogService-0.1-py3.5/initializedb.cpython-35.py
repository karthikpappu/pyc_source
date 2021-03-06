# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/logservice/scripts/initializedb.py
# Compiled at: 2016-10-04 18:00:15
# Size of source mod 2**32: 1537 bytes
from sqlalchemy import create_engine
from logservice import models
from logservice.models.meta import Base
from sqlalchemy.orm import sessionmaker

class InitializeDb(object):

    def __init__(self, connection_string, dbsession=None):
        self.connection_string = connection_string
        self.dbsession = dbsession

    def initialize_db(self):
        if self.dbsession is None:
            engine = create_engine(self.connection_string)
            Base.metadata.drop_all(engine)
            Base.metadata.create_all(engine)
            Session = sessionmaker(bind=engine)
            dbsession = Session()
        else:
            dbsession = self.dbsession
        import logging
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        logger.debug('Initializing Logs')
        from ..models.log import Log
        lg = Log(msg='Initializing Logs')
        dbsession.add(lg)
        dbsession.commit()