# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/ec2/autoscale/request.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 1549 bytes


class Request(object):

    def __init__(self, connection=None):
        self.connection = connection
        self.request_id = ''

    def __repr__(self):
        return 'Request:%s' % self.request_id

    def startElement(self, name, attrs, connection):
        pass

    def endElement(self, name, value, connection):
        if name == 'RequestId':
            self.request_id = value
        else:
            setattr(self, name, value)