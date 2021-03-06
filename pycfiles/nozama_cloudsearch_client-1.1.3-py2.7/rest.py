# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vagrant/src/nozama-cloudsearch/nozama-cloudsearch-client/nozama/cloudsearch/client/rest.py
# Compiled at: 2013-12-03 06:00:21
"""
This provides the REST classes used to access the service.

"""
import json, logging
from urlparse import urljoin
import requests

def get_log(e=None):
    return logging.getLogger(('{0}.{1}').format(__name__, e) if e else __name__)


class CloudSearchService(object):
    """This provides an interface to the REST service for dealing with
    user operations.
    """

    def __init__(self, uri='http://localhost:15808'):
        """Set the URI of the CloudSearchService.

        :param uri: The base address of the remote service server.

        """
        self.log = get_log('CloudSearchService')
        self.uri = uri

    def ping(self):
        """Recover the User Service status page.

        This will raise a connection error or it will return successfully.

        :returns: service status dict.

        """
        res = requests.get(urljoin(self.uri, 'ping'))
        res.raise_for_status()
        return res.json()

    def remove_all(self):
        """Called to remove all documents from the system ready for a new test
        run.
        """
        res = requests.delete(urljoin(self.uri, '/dev/documents'))
        res.raise_for_status()
        return res.json

    def report(self):
        """Called to recover all added and removed documents stored on the
        system.

        """
        res = requests.get(urljoin(self.uri, '/dev/documents'))
        res.raise_for_status()
        return res.json()

    def batch_upload(self, documents):
        """Called to batch load documents into the cloudsearch service.
        """
        uri = urljoin(self.uri, '/2013-08-22/documents/batch')
        documents = json.dumps(documents)
        res = requests.post(uri, data=documents)
        res.raise_for_status()
        return res.json()