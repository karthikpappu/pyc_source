# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ben/Code/plpygis/plpygis/geometry.py
# Compiled at: 2020-02-21 00:21:57
# Size of source mod 2**32: 31056 bytes
from .exceptions import DependencyError, WkbError, SridError, DimensionalityError
from .hex import HexReader, HexWriter, HexBytes
try:
    import shapely.wkb
    from shapely.geos import lgeos, WKBWriter
    SHAPELY = True
except ImportError:
    SHAPELY = False
else:

    class Geometry(object):
        __doc__ = 'A representation of a PostGIS geometry.\n\n    PostGIS geometries are either an OpenGIS Consortium Simple Features for SQL\n    specification type or a PostGIS extended type. The object\'s canonical form\n    is stored in WKB or EWKB format along with an SRID and flags indicating\n    whether the coordinates are 3DZ, 3DM or 4D.\n\n    ``Geometry`` objects can be created in a number of ways. In all cases, a\n    subclass for the particular geometry type will be instantiated.\n\n    From an (E)WKB::\n\n        >>> Geometry(b\'\\x01\\x01\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\')\n        <Point: \'geometry(Point)\'>\n\n    From the hexadecimal string representation of an (E)WKB::\n\n        >>> Geometry("0101000080000000000000000000000000000000000000000000000000")\n        <Point: \'geometry(PointZ)\'>\n\n    The response above indicates an instance of the ``Point`` class has been\n    created and that it represents a PostGIS ``geometry(PointZ)`` type.\n\n    From a GeoJSON::\n\n        >>> Geometry.from_geojson({\'type\': \'Point\', \'coordinates\': (0.0, 0.0)})\n        <Point: \'geometry(Point,4326)\'>\n\n    From a Shapely object::\n\n        >>> from shapely.geometry import Point\n        >>> Geometry.from_shapely(Point((0, 0)), 3857)\n        <Point: \'geometry(Point,3857)\'>\n\n    From any object supporting ``__geo_interface__``::\n\n        >>> from shapefile import Reader\n        >>> feature = Reader("test/multipoint.shp").shape(0)\n        >>> Geometry.shape(feature)\n        <MultiPoint: \'geometry(MultiPoint)\'>\n\n    A ``Geometry`` can be read as long as it is one of the following\n    types: ``Point``, ``LineString``, ``Polygon``, ``MultiPoint``, ``MultiLineString``,\n    ``MultiPolygon`` or ``GeometryCollection``. The M dimension will be preserved.\n    '
        _WKBTYPE = 536870911
        _WKBZFLAG = 2147483648
        _WKBMFLAG = 1073741824
        _WKBSRIDFLAG = 536870912
        __slots__ = ['_wkb', '_reader', '_srid', '_dimz', '_dimm']

        def __new__(cls, wkb, srid=None, dimz=False, dimm=False):
            if cls == Geometry:
                if not wkb:
                    raise WkbError('No EWKB provided')
                wkb = HexBytes(wkb)
                newcls, dimz, dimm, srid, reader = Geometry._from_wkb(wkb)
                geom = super(Geometry, cls).__new__(newcls)
                geom._wkb = wkb
                geom._reader = reader
                geom._srid = srid
                geom._dimz = dimz
                geom._dimm = dimm
            else:
                geom = super(Geometry, cls).__new__(cls)
                geom._wkb = None
                geom._reader = None
            return geom

        @staticmethod
        def from_geojson(geojson, srid=4326):
            """
        Create a Geometry from a GeoJSON. The SRID can be overridden from the
        expected 4326.
        """
            type_ = geojson['type'].lower()
            if type_ == 'geometrycollection':
                geometries = []
                for geometry in geojson['geometries']:
                    geometries.append(Geometry.from_geojson(geometry, srid=None))
                else:
                    return GeometryCollection(geometries, srid)

            if type_ == 'point':
                return Point((geojson['coordinates']), srid=srid)
            if type_ == 'linestring':
                return LineString((geojson['coordinates']), srid=srid)
            if type_ == 'polygon':
                return Polygon((geojson['coordinates']), srid=srid)
            if type_ == 'multipoint':
                geometries = _MultiGeometry._multi_from_geojson(geojson, Point)
                return MultiPoint(geometries, srid=srid)
            if type_ == 'multilinestring':
                geometries = _MultiGeometry._multi_from_geojson(geojson, LineString)
                return MultiLineString(geometries, srid=srid)
            if type_ == 'multipolygon':
                geometries = _MultiGeometry._multi_from_geojson(geojson, Polygon)
                return MultiPolygon(geometries, srid=srid)

        @staticmethod
        def from_shapely(sgeom, srid=None):
            """
        Create a Geometry from a Shapely geometry and the specified SRID.

        The Shapely geometry will not be modified.
        """
            if SHAPELY:
                WKBWriter.defaults['include_srid'] = True
                if srid:
                    lgeos.GEOSSetSRID(sgeom._geom, srid)
                return Geometry(sgeom.wkb_hex)
            raise DependencyError('Shapely')

        @staticmethod
        def shape(shape, srid=None):
            """
        Create a Geometry using ``__geo_interface__`` and the specified SRID.
        """
            return Geometry.from_geojson(shape.__geo_interface__, srid)

        @property
        def type(self):
            """
        The geometry type.
        """
            return self.__class__.__name__

        @property
        def srid(self):
            """
        The geometry SRID.
        """
            return self._srid

        @srid.setter
        def srid(self, value):
            self._check_cache()
            self._srid = value

        @property
        def geojson(self):
            """
        Get the geometry as a GeoJSON dict. There is no check that the
        GeoJSON is using an SRID of 4326.
        """
            return self._to_geojson(dimz=(self.dimz))

        @property
        def wkb(self):
            """
        Get the geometry as an (E)WKB.
        """
            return self._to_wkb(use_srid=True, dimz=(self.dimz), dimm=(self.dimm))

        @property
        def shapely(self):
            """
        Get the geometry as a Shapely geometry. If the geometry has an SRID,
        the Shapely object will be created with it set.
        """
            return self._to_shapely()

        @property
        def bounds(self):
            """
        Get the minimum and maximum extents of the geometry: (minx, miny, maxx,
        maxy).
        """
            return self._bounds()

        @property
        def postgis_type(self):
            """
        Get the type of the geometry in PostGIS format, including additional
        dimensions and SRID if they exist.
        """
            dimz = 'Z' if self.dimz else ''
            dimm = 'M' if self.dimm else ''
            if self.srid:
                return 'geometry({}{}{},{})'.format(self.type, dimz, dimm, self.srid)
            return 'geometry({}{}{})'.format(self.type, dimz, dimm)

        @staticmethod
        def _from_wkb(wkb):
            try:
                if wkb.startswith(b'\x00'):
                    reader = HexReader(wkb, '>')
                else:
                    if wkb.startswith(b'\x01'):
                        reader = HexReader(wkb, '<')
                    else:
                        raise WkbError('First byte in WKB must be 0 or 1.')
            except TypeError:
                raise WkbError()
            else:
                return Geometry._get_wkb_type(reader) + (reader,)

        def _check_cache(self):
            if self._reader is not None:
                self._load_geometry()
                self._wkb = None
                self._reader = None

        def _to_wkb(self, use_srid, dimz, dimm):
            if self._wkb is not None:
                return self._wkb
            writer = HexWriter('<')
            self._write_wkb_header(writer, use_srid, dimz, dimm)
            self._write_wkb(writer, dimz, dimm)
            return writer.data

        def _to_shapely(self):
            if SHAPELY:
                sgeom = shapely.wkb.loads(self.wkb)
                srid = lgeos.GEOSGetSRID(sgeom._geom)
                if srid == 0:
                    srid = None
                elif srid or self.srid:
                    if srid != self.srid:
                        raise SridError('SRID mismatch: {} {}'.format(srid, self.srid))
                return sgeom
            raise DependencyError('Shapely')

        def _to_geojson(self, dimz):
            coordinates = self._to_geojson_coordinates(dimz)
            geojson = {'type':self.type, 
             'coordinates':coordinates}
            return geojson

        def __repr__(self):
            return "<{}: '{}'>".format(self.type, self.postgis_type)

        def __str__(self):
            return self.wkb.__str__()

        @property
        def __geo_interface__(self):
            return self.geojson

        def _set_dimensionality(self, geometries):
            self._dimz = None
            self._dimm = None
            for geometry in geometries:
                if self._dimz is None:
                    self._dimz = geometry.dimz
                else:
                    if self._dimz != geometry.dimz:
                        raise DimensionalityError('Mixed dimensionality in MultiGeometry')
                if self._dimm is None:
                    self._dimm = geometry.dimm
                elif self._dimm != geometry.dimm:
                    raise DimensionalityError('Mixed dimensionality in MultiGeometry')

        @staticmethod
        def _get_wkb_type(reader):
            lwgeomtype, dimz, dimm, srid = Geometry._read_wkb_header(reader)
            if lwgeomtype == 1:
                cls = Point
            else:
                if lwgeomtype == 2:
                    cls = LineString
                else:
                    if lwgeomtype == 3:
                        cls = Polygon
                    else:
                        if lwgeomtype == 4:
                            cls = MultiPoint
                        else:
                            if lwgeomtype == 5:
                                cls = MultiLineString
                            else:
                                if lwgeomtype == 6:
                                    cls = MultiPolygon
                                else:
                                    if lwgeomtype == 7:
                                        cls = GeometryCollection
                                    else:
                                        raise WkbError('Unsupported WKB type: {}'.format(lwgeomtype))
            return (
             cls, dimz, dimm, srid)

        @staticmethod
        def _read_wkb_header(reader):
            try:
                reader.get_char()
                header = reader.get_int()
                lwgeomtype = header & Geometry._WKBTYPE
                dimz = bool(header & Geometry._WKBZFLAG)
                dimm = bool(header & Geometry._WKBMFLAG)
                if header & Geometry._WKBSRIDFLAG:
                    srid = reader.get_int()
                else:
                    srid = None
            except TypeError:
                raise WkbError()
            else:
                return (
                 lwgeomtype, dimz, dimm, srid)

        def _write_wkb_header(self, writer, use_srid, dimz, dimm):
            writer.add_order()
            header = self._LWGEOMTYPE | (Geometry._WKBZFLAG if dimz else 0) | (Geometry._WKBMFLAG if dimm else 0) | (Geometry._WKBSRIDFLAG if self.srid else 0)
            writer.add_int(header)
            if use_srid:
                if self.srid:
                    writer.add_int(self.srid)
            return writer


    class _MultiGeometry(Geometry):

        @property
        def dimz(self):
            """
        Whether the geometry has a Z dimension.

        :getter: ``True`` if the geometry has a Z dimension.
        :setter: Add or remove the Z dimension from this and all geometries in the collection.
        :rtype: bool
        """
            return self._dimz

        @dimz.setter
        def dimz(self, value):
            if self._dimz == value:
                return
            for geometry in self.geometries:
                geometry.dimz = value
            else:
                self._dimz = value

        @property
        def dimm(self):
            """
        Whether the geometry has an M dimension.

        :getter: ``True`` if the geometry has an M dimension.
        :setter: Add or remove the M dimension from this and all geometries in the collection.
        :rtype: bool
       """
            return self._dimm

        @dimm.setter
        def dimm(self, value):
            if self._dimm == value:
                return
            for geometry in self.geometries:
                geometry.dimm = value
            else:
                self._dimm = value

        def _bounds(self):
            bounds = [g.bounds for g in self.geometries]
            minx = min([b[0] for b in bounds])
            miny = min([b[1] for b in bounds])
            maxx = max([b[2] for b in bounds])
            maxy = max([b[3] for b in bounds])
            return (minx, miny, maxx, maxy)

        @staticmethod
        def _multi_from_geojson(geojson, cls):
            geometries = []
            for coordinates in geojson['coordinates']:
                geometry = cls(coordinates, srid=None)
                geometries.append(geometry)
            else:
                return geometries

        def _load_geometry(self):
            self._geometries = self.__class__._read_wkb(self._reader, self._dimz, self._dimm)

        def _set_multi_metadata(self):
            self._dimz = None
            self._dimm = None
            for geometry in self.geometries:
                if self._dimz is None:
                    self._dimz = geometry.dimz
                else:
                    if self._dimz != geometry.dimz:
                        raise DimensionalityError('Mixed dimensionality in MultiGeometry')
                    elif self._dimm is None:
                        self._dimm = geometry.dimm
                    else:
                        if self._dimm != geometry.dimm:
                            raise DimensionalityError('Mixed dimensionality in MultiGeometry')
                if self.srid is None:
                    if geometry._srid is not None:
                        self._srid = geometry.srid
                elif self.srid != geometry.srid:
                    if geometry.srid is not None:
                        raise SridError('Mixed SRIDs in MultiGeometry')

        def _to_geojson_coordinates(self, dimz):
            coordinates = [g._to_geojson_coordinates(dimz=dimz) for g in self.geometries]
            return coordinates

        @staticmethod
        def _read_wkb(reader, dimz, dimm):
            geometries = []
            try:
                for _ in range(reader.get_int()):
                    cls, dimz, dimm, srid = Geometry._get_wkb_type(reader)
                    coordinates = cls._read_wkb(reader, dimz, dimm)
                    geometry = cls(coordinates, srid=srid, dimz=dimz, dimm=dimm)
                    geometries.append(geometry)

            except TypeError:
                raise WkbError()
            else:
                return geometries

        def _write_wkb(self, writer, dimz, dimm):
            writer.add_int(len(self.geometries))
            for geometry in self.geometries:
                geometry._write_wkb_header(writer, False, dimz, dimm)
                geometry._write_wkb(writer, dimz, dimm)


    class Point(Geometry):
        __doc__ = "\n    A representation of a PostGIS Point.\n\n    ``Point`` objects can be created directly.\n\n        >>> Point((0, -52, 5), dimm=True, srid=4326)\n        <Point: 'geometry(PointM,4326)'>\n\n    The ``dimz`` and ``dimm`` parameters will indicate how to interpret the\n    coordinates that have been passed as the first argument. By default, the\n    third coordinate will be interpreted as representing the Z dimension.\n    "
        _LWGEOMTYPE = 1
        __slots__ = ['_x', '_y', '_z', '_m']

        def __init__(self, coordinates=None, srid=None, dimz=False, dimm=False):
            if self._wkb:
                self._x = None
                self._y = None
                self._z = None
                self._m = None
            else:
                self._srid = srid
                coordinates = list(coordinates)
                self._x = coordinates[0]
                self._y = coordinates[1]
                num = len(coordinates)
                if num > 4:
                    raise DimensionalityError('Maximum dimensionality supported for coordinates is 4: {}'.format(coordinates))
                else:
                    if num == 2:
                        if dimz and dimm:
                            self._z = 0
                            self._m = 0
                        else:
                            if dimz:
                                self._z = 0
                                self._m = None
                            else:
                                if dimm:
                                    self._z = None
                                    self._m = 0
                                else:
                                    self._z = None
                                    self._m = None
                    else:
                        if num == 3:
                            if dimz and dimm:
                                self._z = coordinates[2]
                                self._m = 0
                            else:
                                if dimm:
                                    self._z = None
                                    self._m = coordinates[2]
                                else:
                                    self._z = coordinates[2]
                                    self._m = None
                        else:
                            self._z = coordinates[2]
                            self._m = coordinates[3]
                self._dimz = self._z is not None
                self._dimm = self._m is not None

        @property
        def x(self):
            """
        X coordinate.
        """
            self._check_cache()
            return self._x

        @x.setter
        def x(self, value):
            self._check_cache()
            self._x = value

        @property
        def y(self):
            """
        M coordinate.
        """
            self._check_cache()
            return self._y

        @y.setter
        def y(self, value):
            self._check_cache()
            self._y = value

        @property
        def z(self):
            """
        Z coordinate.
        """
            if not self._dimz:
                return
            self._check_cache()
            return self._z

        @z.setter
        def z(self, value):
            self._check_cache()
            self._z = value
            if value is None:
                self._dimz = False
            else:
                self._dimz = True

        @property
        def m(self):
            """
        M coordinate.
        """
            if not self._dimm:
                return
            self._check_cache()
            return self._m

        @m.setter
        def m(self, value):
            self._check_cache()
            self._m = value
            if value is None:
                self._dimm = False
            else:
                self._dimm = True

        @property
        def dimz(self):
            """
        Whether the geometry has a Z dimension.

        :getter: ``True`` if the geometry has a Z dimension.
        :setter: Add or remove the Z dimension.
        :rtype: bool
        """
            return self._dimz

        @dimz.setter
        def dimz(self, value):
            if self._dimz == value:
                return
            self._check_cache()
            if value and self._z is None:
                self._z = 0
            else:
                if value is None:
                    self._z = None
            self._dimz = value

        @property
        def dimm(self):
            """
        Whether the geometry has an M dimension.

        :getter: ``True`` if the geometry has an M dimension.
        :setter: Add or remove the M dimension.
        :rtype: bool
        """
            return self._dimm

        @dimm.setter
        def dimm(self, value):
            if self._dimm == value:
                return
            self._check_cache()
            if value and self._m is None:
                self._m = 0
            else:
                if value is None:
                    self._m = None
            self._dimm = value

        def _to_geojson_coordinates(self, dimz):
            coordinates = [
             self.x, self.y]
            if dimz:
                coordinates.append(self.z)
            return coordinates

        def _bounds(self):
            return (
             self.x, self.y, self.x, self.y)

        def _load_geometry(self):
            self._x, self._y, self._z, self._m = Point._read_wkb(self._reader, self._dimz, self._dimm)

        @staticmethod
        def _read_wkb(reader, dimz, dimm):
            try:
                x = reader.get_double()
                y = reader.get_double()
                if dimz and dimm:
                    z = reader.get_double()
                    m = reader.get_double()
                else:
                    if dimz:
                        z = reader.get_double()
                        m = None
                    else:
                        if dimm:
                            z = None
                            m = reader.get_double()
                        else:
                            z = None
                            m = None
            except TypeError:
                raise WkbError()
            else:
                return (
                 x, y, z, m)

        def _write_wkb(self, writer, dimz, dimm):
            writer.add_double(self.x)
            writer.add_double(self.y)
            if dimz and dimm:
                writer.add_double(self.z)
                writer.add_double(self.m)
            else:
                if dimz:
                    writer.add_double(self.z)
                else:
                    if dimm:
                        writer.add_double(self.m)


    class LineString(Geometry):
        __doc__ = "\n    A representation of a PostGIS Line.\n\n    ``LineString`` objects can be created directly.\n\n        >>> LineString([(0, 0, 0, 0), (1, 1, 0, 0), (2, 2, 0, 0)])\n        <LineString: 'geometry(LineStringZM)'>\n\n    The ``dimz`` and ``dimm`` parameters will indicate how to interpret the\n    coordinates that have been passed as the first argument. By default, the\n    third coordinate will be interpreted as representing the Z dimension.\n    "
        _LWGEOMTYPE = 2
        __slots__ = ['_vertices']

        def __init__(self, vertices=None, srid=None, dimz=False, dimm=False):
            if self._wkb:
                self._vertices = None
            else:
                self._srid = srid
                self._dimz = dimz
                self._dimm = dimm
                self._vertices = LineString._from_coordinates(vertices, dimz=dimz, dimm=dimm)
                self._set_dimensionality(self._vertices)

        @property
        def vertices(self):
            """
        List of vertices that comprise the line.
        """
            self._check_cache()
            return self._vertices

        @property
        def dimz(self):
            """
        Whether the geometry has a Z dimension.

        :getter: ``True`` if the geometry has a Z dimension.
        :setter: Add or remove the Z dimension from this and all vertices in the line.
        :rtype: bool
        """
            return self._dimz

        @dimz.setter
        def dimz(self, value):
            if self.dimz == value:
                return
            for vertex in self.vertices:
                vertex.dimz = value
            else:
                self._dimz = value

        @property
        def dimm(self):
            """
        Whether the geometry has a M dimension.

        :getter: ``True`` if the geometry has a M dimension.
        :setter: Add or remove the M dimension from this and all vertices in the line.
        :rtype: bool
        """
            return self._dimm

        @dimm.setter
        def dimm(self, value):
            if self.dimm == value:
                return
            for vertex in self.vertices:
                vertex.dimm = value
            else:
                self._dimm = value

        def _to_geojson_coordinates(self, dimz):
            coordinates = [v._to_geojson_coordinates(dimz=dimz) for v in self.vertices]
            return coordinates

        def _bounds(self):
            x = [v.x for v in self.vertices]
            y = [v.y for v in self.vertices]
            return (min(x), min(y), max(x), max(y))

        @staticmethod
        def _from_coordinates(vertices, dimz, dimm):
            return [Point(vertex, dimz=dimz, dimm=dimm) for vertex in vertices]

        def _load_geometry(self):
            vertices = LineString._read_wkb(self._reader, self._dimz, self._dimm)
            self._vertices = LineString._from_coordinates(vertices, self._dimz, self._dimm)

        @staticmethod
        def _read_wkb(reader, dimz, dimm):
            vertices = []
            try:
                for _ in range(reader.get_int()):
                    coordinates = Point._read_wkb(reader, dimz, dimm)
                    vertices.append(coordinates)

            except TypeError:
                raise WkbError()
            else:
                return vertices

        def _write_wkb(self, writer, dimz, dimm):
            writer.add_int(len(self.vertices))
            for vertex in self.vertices:
                vertex._write_wkb(writer, dimz, dimm)


    class Polygon(Geometry):
        __doc__ = "\n    A representation of a PostGIS Polygon.\n\n    ``Polygon`` objects can be created directly.\n\n        >>> Polygon([[(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0), (0, 0, 0)]])\n        <Polygon: 'geometry(PolygonZ)'>\n\n    The first polygon in the list of linear rings is the exterior ring, while\n    any subsequent rings are interior boundaries.\n\n    The ``dimz`` and ``dimm`` parameters will indicate how to interpret the\n    coordinates that have been passed as the first argument. By default, the\n    third coordinate will be interpreted as representing the Z dimension.\n    "
        _LWGEOMTYPE = 3
        __slots__ = ['_rings']

        def __init__(self, rings=None, srid=None, dimz=False, dimm=False):
            if self._wkb:
                self._rings = None
            else:
                self._srid = srid
                self._dimz = dimz
                self._dimm = dimm
                self._rings = Polygon._from_coordinates(rings, dimz, dimm)
                self._set_dimensionality(self._rings)

        @property
        def rings(self):
            """
        List of linearrings that comprise the polygon.
        """
            self._check_cache()
            return self._rings

        @property
        def exterior(self):
            """
        The exterior ring of the polygon.
        """
            return self.rings[0]

        @property
        def interior(self):
            """
        A list of interior rings of the polygon.
        """
            return self.rings[1:]

        @property
        def dimz(self):
            """
        Whether the geometry has a Z dimension.

        :getter: ``True`` if the geometry has a Z dimension.
        :setter: Add or remove the Z dimension from this and all linear rings in the polygon.
        :rtype: bool
        """
            return self._dimz

        @dimz.setter
        def dimz(self, value):
            if self._dimz == value:
                return
            for ring in self.rings:
                ring.dimz = value
            else:
                self._dimz = value

        @property
        def dimm(self):
            """
        Whether the geometry has a M dimension.

        :getter: ``True`` if the geometry has a M dimension.
        :setter: Add or remove the M dimension from this and all linear rings in the polygon.
        :rtype: bool
        """
            return self._dimm

        @dimm.setter
        def dimm(self, value):
            if self._dimm == value:
                return
            for ring in self.rings:
                ring.dimm = value
            else:
                self._dimm = value

        def _to_geojson_coordinates(self, dimz):
            coordinates = [r._to_geojson_coordinates(dimz=dimz) for r in self.rings]
            return coordinates

        def _bounds(self):
            return self.exterior.bounds

        @staticmethod
        def _from_coordinates(rings, dimz, dimm):
            return [LineString(vertices, dimz, dimm) for vertices in rings]

        def _load_geometry(self):
            rings = Polygon._read_wkb(self._reader, self._dimz, self._dimm)
            self._rings = Polygon._from_coordinates(rings, self._dimz, self._dimm)

        @staticmethod
        def _read_wkb(reader, dimz, dimm):
            rings = []
            try:
                for _ in range(reader.get_int()):
                    vertices = LineString._read_wkb(reader, dimz, dimm)
                    rings.append(vertices)

            except TypeError:
                raise WkbError()
            else:
                return rings

        def _write_wkb(self, writer, dimz, dimm):
            writer.add_int(len(self.rings))
            for ring in self.rings:
                ring._write_wkb(writer, dimz, dimm)


    class MultiPoint(_MultiGeometry):
        __doc__ = "\n    A representation of a PostGIS MultiPoint.\n\n    ``MultiPoint`` objects can be created directly from a list of ``Point``\n    objects.\n\n        >>> p1 = Point((0, 0, 0))\n        >>> p2 = Point((1, 1, 0))\n        >>> MultiPoint([p1, p2])\n        <MultiPoint: 'geometry(MultiPointZ)'>\n\n    The dimensionality of all geometries in the collection must be identical.\n    "
        _LWGEOMTYPE = 4
        __slots__ = ['_points']

        def __init__(self, points=None, srid=None):
            if self._wkb:
                self._points = None
            else:
                self._points = points
                self._srid = srid
                self._set_multi_metadata()

        @property
        def points(self):
            """
        List of all component points.
        """
            self._check_cache()
            return self._points

        @property
        def geometries(self):
            """
        List of all component points.
        """
            return self.points

        def _load_geometry(self):
            self._points = MultiPoint._read_wkb(self._reader, self._dimz, self._dimm)


    class MultiLineString(_MultiGeometry):
        __doc__ = "\n    A representation of a PostGIS MultiLineString\n\n    ``MultiLineString`` objects can be created directly from a list of\n    ``LineString`` objects.\n\n        >>> l1 = LineString([(1, 1, 0), (2, 2, 0)], dimm=True)\n        >>> l2 = LineString([(0, 0, 0), (0, 1, 0)], dimm=True)\n        >>> MultiLineString([l1, l2])\n        <MultiLineString: 'geometry(MultiLineStringM)'>\n\n    The dimensionality of all geometries in the collection must be identical.\n    "
        _LWGEOMTYPE = 5
        __slots__ = ['_linestrings']

        def __init__(self, linestrings=None, srid=None):
            if self._wkb:
                self._linestrings = None
            else:
                self._linestrings = linestrings
                self._srid = srid
                self._set_multi_metadata()

        @property
        def linestrings(self):
            """
        List of all component lines.
        """
            self._check_cache()
            return self._linestrings

        @property
        def geometries(self):
            """
        List of all component lines.
        """
            return self.linestrings

        def _load_geometry(self):
            self._linestrings = MultiLineString._read_wkb(self._reader, self._dimz, self._dimm)


    class MultiPolygon(_MultiGeometry):
        __doc__ = "\n    A representation of a PostGIS MultiPolygon.\n\n    ``MultiPolygon`` objects can be created directly from a list of ``Polygon``\n    objects.\n\n        >>> p1 = Polygon([[(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)]], srid=4326)\n        >>> p2 = Polygon([[(2, 2), (3, 2), (3, 3), (2, 3), (2, 2)]], srid=4326)\n        >>> MultiPolygon([p1, p2])\n        <MultiPolygon: 'geometry(MultiPolygon,4326)'>\n\n    The dimensionality of all geometries in the collection must be identical.\n    "
        _LWGEOMTYPE = 6
        __slots__ = ['__polygons__']

        def __init__(self, polygons=None, srid=None, dimz=False, dimm=False):
            if self._wkb:
                self._polygons = None
            else:
                self._srid = srid
                self._dimz = dimz
                self._dimm = dimm
                self._polygons = polygons
                self._set_multi_metadata()

        @property
        def polygons(self):
            """
        List of all component polygons.
        """
            self._check_cache()
            return self._polygons

        @property
        def geometries(self):
            """
        List of all component polygons.
        """
            return self.polygons

        def _load_geometry(self):
            self._polygons = MultiPolygon._read_wkb(self._reader, self._dimz, self._dimm)


    class GeometryCollection(_MultiGeometry):
        __doc__ = "\n    A representation of a PostGIS GeometryCollection.\n\n    ``GeometryCollection`` objects can be created directly from a list of\n    geometries, including other collections.\n\n        >>> p = Point((0, 0, 0))\n        >>> l = LineString([(1, 1, 0), (2, 2, 0)])\n        >>> GeometryCollection([p, l])\n        <GeometryCollection: 'geometry(GeometryCollectionZ)'>\n\n    The dimensionality of all geometries in the collection must be identical.\n    "
        _LWGEOMTYPE = 7
        __slots__ = ['_geometries']

        def __init__(self, geometries=None, srid=None, dimz=False, dimm=False):
            if self._wkb:
                self._geometries = None
            else:
                self._geometries = geometries
                self._srid = srid
                self._set_multi_metadata()

        @property
        def geometries(self):
            """
        List of all component geometries.
        """
            self._check_cache()
            return self._geometries

        def _to_geojson(self, dimz):
            geometries = [g._to_geojson(dimz=dimz) for g in self.geometries]
            geojson = {'type':self.__class__.__name__, 
             'geometries':geometries}
            return geojson