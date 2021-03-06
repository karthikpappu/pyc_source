# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/FeatureServer/Feature/Feature.py
# Compiled at: 2008-01-01 03:15:59
__author__ = 'MetaCarta'
__copyright__ = 'Copyright (c) 2006-2008 MetaCarta'
__license__ = 'Clear BSD'
__version__ = '$Id: Feature.py 412 2008-01-01 08:15:59Z crschmidt $'
import sys

class Feature(object):
    __module__ = __name__

    def __init__(self, id=None, geometry=None, props=None):
        self.id = id
        self.geometry = geometry or {}
        self.properties = props or {}
        self.bbox = None
        return

    def get_bbox(self):
        minx = miny = sys.maxint
        maxx = maxy = -1 * sys.maxint
        try:
            coords = self.geometry['coordinates']
            if self.geometry['type'] in ('Point', 'Line'):
                for coord in coords:
                    if coord[0] < minx:
                        minx = coord[0]
                    if coord[0] > maxx:
                        maxx = coord[0]
                    if coord[1] < miny:
                        miny = coord[1]
                    if coord[1] > maxy:
                        maxy = coord[1]

            for ring in coords:
                for coord in ring:
                    if coord[0] < minx:
                        minx = coord[0]
                    if coord[0] > maxx:
                        maxx = coord[0]
                    if coord[1] < miny:
                        miny = coord[1]
                    if coord[1] > maxy:
                        maxy = coord[1]

            return (
             minx, miny, maxx, maxy)
        except:
            raise Exception('Unable to determine bounding box for feature with geometry %s' % self.geometry)

    def to_dict(self):
        return {'id': self.id, 'geometry': self.geometry, 'properties': self.properties}