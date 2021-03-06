# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cptsoul/sendfile/protocol.py
# Compiled at: 2014-01-02 09:45:24
import logging
from twisted.internet.protocol import Protocol, connectionDone
from cptsoul.sendfile.producer import Producer

class SendProtocol(Protocol):

    def __init__(self, path, progressCallback, endCallback, errorCallback):
        self._path = path
        self._progressCallback = progressCallback
        self._endCallback = endCallback
        self._errorCallback = errorCallback
        self._allGood = False

    def connectionMade(self):
        logging.info('SendFile : Connected')
        producer = Producer(self, self._path, self._progressCallback)
        self.transport.registerProducer(producer, True)
        producer.resumeProducing()

    def connectionLost(self, reason=connectionDone):
        if self._allGood:
            logging.info('SendFile : File sended')
            self._endCallback()
        else:
            logging.warning('SendFile : Error sending')
            self._errorCallback()

    def setAllGood(self):
        self._allGood = True