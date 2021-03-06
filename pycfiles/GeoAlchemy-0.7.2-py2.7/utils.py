# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/geoalchemy/utils.py
# Compiled at: 2013-01-09 17:05:16
import re

def from_wkt(geom):
    """wkt helper: converts from WKT to a GeoJSON-like geometry."""
    wkt_linestring_match = re.compile('\\(([^()]+)\\)')
    re_space = re.compile('\\s+')
    coords = []
    for line in wkt_linestring_match.findall(geom):
        rings = [[]]
        for pair in line.split(','):
            if not pair.strip():
                rings.append([])
                continue
            rings[(-1)].append(map(float, re.split(re_space, pair.strip())))

        coords.append(rings[0])

    if geom.startswith('MULTIPOINT'):
        geomtype = 'MultiPoint'
        coords = coords[0]
    elif geom.startswith('POINT'):
        geomtype = 'Point'
        coords = coords[0][0]
    elif geom.startswith('MULTILINESTRING'):
        geomtype = 'MultiLineString'
    elif geom.startswith('LINESTRING'):
        geomtype = 'LineString'
        coords = coords[0]
    elif geom.startswith('MULTIPOLYGON'):
        geomtype = 'MultiPolygon'
    elif geom.startswith('POLYGON'):
        geomtype = 'Polygon'
    else:
        geomtype = geom[:geom.index('(')]
        raise Exception('Unsupported geometry type %s' % geomtype)
    return {'type': geomtype, 'coordinates': coords}


def to_wkt(geom):
    """Converts a GeoJSON-like geometry to WKT."""

    def coords_to_wkt(coords):
        format_str = (' ').join(('%f', ) * len(coords[0]))
        return (',').join([ format_str % tuple(c) for c in coords ])

    coords = geom['coordinates']
    if geom['type'] == 'Point':
        return 'POINT(%s)' % coords_to_wkt((coords,))
    if geom['type'] == 'LineString':
        return 'LINESTRING (%s)' % coords_to_wkt(coords)
    if geom['type'] == 'Polygon':
        rings = [ '(' + coords_to_wkt(ring) + ')' for ring in coords ]
        rings = (',').join(rings)
        return 'POLYGON(%s)' % rings
    if geom['type'] == 'MultiPoint':
        pts = (',').join(coords_to_wkt((ring,)) for ring in coords)
        return 'MULTIPOINT(%s)' % str(pts)
    if geom['type'] == 'MultiLineString':
        pts = (',').join('(' + coords_to_wkt(ring) + ')' for ring in coords)
        return 'MultiLineString(%s)' % str(pts)
    if geom['type'] == 'MultiPolygon':
        poly_str = []
        for coord_list in coords:
            poly_str.append('((' + (',').join(coords_to_wkt((ring,)) for ring in coord_list) + '))')

        return 'MultiPolygon(%s)' % (', ').join(poly_str)
    raise Exception("Couldn't create WKT from geometry of type %s (%s). Only Point, Line, Polygon are supported." % (geom['type'], geom))