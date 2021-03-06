# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/ec2/cloudwatch/datapoint.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 1668 bytes
from datetime import datetime

class Datapoint(dict):

    def __init__(self, connection=None):
        dict.__init__(self)
        self.connection = connection

    def startElement(self, name, attrs, connection):
        pass

    def endElement(self, name, value, connection):
        if name in ('Average', 'Maximum', 'Minimum', 'Sum', 'SampleCount'):
            self[name] = float(value)
        else:
            if name == 'Timestamp':
                self[name] = datetime.strptime(value, '%Y-%m-%dT%H:%M:%SZ')
            elif name != 'member':
                self[name] = value