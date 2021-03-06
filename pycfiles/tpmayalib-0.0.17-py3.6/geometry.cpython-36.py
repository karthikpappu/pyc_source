# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpMayaLib/core/geometry.py
# Compiled at: 2020-01-16 21:52:40
# Size of source mod 2**32: 21809 bytes
"""
Module that contains functions and classes related with geometry
"""
from __future__ import print_function, division, absolute_import
import logging
from tpPyUtils import mathlib, python
import tpMayaLib as maya
from tpMayaLib.core import api, exceptions, shape, transform as xform_utils, name as name_utils
LOGGER = logging.getLogger()

class MeshTopologyCheck(object):

    def __init__(self, mesh1, mesh2):
        self.mesh1 = None
        self.mesh1_function = None
        self.mesh1_vert_count = None
        self.mesh1_edge_count = None
        self.mesh1_face_count = None
        self.mesh2 = None
        self.mesh2_function = None
        self.mesh2_vert_count = None
        self.mesh2_edge_count = None
        self.mesh2_face_count = None
        self.set_first_mesh(mesh1)
        self.set_second_mesh(mesh2)

    def set_first_mesh(self, mesh):
        """
        Sets the first mesh to compare
        :param mesh: str, name of  the mesh
        """
        self.mesh1 = get_mesh_shape(mesh, 0)
        self.mesh1_function = api.MeshFunction(self.mesh1)
        self.mesh1_vert_count = self.mesh1_function.get_number_of_vertices()
        self.mesh1_edge_count = self.mesh1_function.get_number_of_edges()
        self.mesh1_face_count = self.mesh1_function.get_number_of_faces()

    def set_second_mesh(self, mesh):
        """
        Sets the second mesh to compare
        :param mesh: str, name of  the mesh
        """
        self.mesh2 = get_mesh_shape(mesh, 0)
        self.mesh2_function = api.MeshFunction(self.mesh2)
        self.mesh2_vert_count = self.mesh2_function.get_number_of_vertices()
        self.mesh2_edge_count = self.mesh2_function.get_number_of_edges()
        self.mesh2_face_count = self.mesh2_function.get_number_of_faces()

    def check_vert_count(self):
        """
        Returns whether both meshes have same number of vertices
        :return: bool
        """
        return self.mesh1_vert_count == self.mesh2_vert_count

    def check_edge_count(self):
        """
        Returns whether both meshes have same number of edges
        :return: bool
        """
        return self.mesh1_edge_count == self.mesh2_edge_count

    def check_face_count(self):
        """
        Returns whether both meshes have same number of faces
        :return: bool
        """
        return self.mesh1_face_count == self.mesh2_face_count

    def check_vert_face_count(self):
        """
        Returns whether both meshes have same number of faces and vertices
        :return: bool
        """
        if not self.check_face_count():
            return False
        else:
            if not self.check_vert_count():
                return False
            return True

    def check_vert_edge_face_count(self):
        """
        Returns whether both meshes have same number of faces, vertices and edges
        :return: bool
        """
        if not self.check_face_count():
            return False
        else:
            if not self.check_vert_count():
                return False
            if not self.check_edge_count():
                return False
            return True

    def check_first_face_verts(self):
        """
        Returns whether both meshes have the same first face index
        :return: bool
        """
        face1 = faces_to_vertices('%s.f[0]' % self.mesh1)
        face2 = faces_to_vertices('%s.f[0]' % self.mesh2)
        vertex_indices1 = get_vertex_indices(face1)
        vertex_indices2 = get_vertex_indices(face2)
        return vertex_indices1 == vertex_indices2


def check_geometry(geometry):
    """
    Checks if a node is valid geometry node and raise and exception if the node is not valid
    :param geometry: str, name of the node to be checked
    :return: bool, True if the give node is a geometry node
    """
    if not is_geometry(geometry):
        raise exceptions.GeometryException(geometry)


def is_a_surface(geometry):
    """
    Returns whether given nodo is a surface one or not
    :param geometry: str
    :return: bopol
    """
    return maya.cmds.objExists('{}.cv[0][0]'.format(geometry))


def is_geometry(geometry):
    """
    Check if the given node is a valid geometry shape node
    :param geometry: str, node object to query as geometry
    :return: bool
    """
    if not maya.cmds.objExists(geometry):
        return False
    else:
        if 'transform' in maya.cmds.nodeType(geometry, i=True):
            geo_shape = maya.cmds.ls((maya.cmds.listRelatives(geometry, s=True, ni=True, pa=True) or []), geometry=True)
            if not geo_shape:
                return False
            geometry = geo_shape[0]
        if 'geometryShape' in maya.cmds.nodeType(geometry, i=True):
            return True
        return False


def geometry_type(geometry):
    """
    Returns the geometry type of the first shape under the given geometry object
    :param geometry: str, geometry object to query
    :return: str
    """
    if not maya.cmds.objExists(geometry):
        raise exceptions.GeometryExistsException(geometry)
    else:
        shapes_list = shape.get_shapes(node=geometry, intermediates=False)
        if not shapes_list:
            shapes_list = shape.get_shapes(node=geometry, intermediates=True)
        raise shapes_list or exceptions.NoShapeChildren(geometry)
    geometry_type = maya.cmds.objectType(shapes_list[0])
    return geometry_type


def component_type(geometry):
    """
    Rreturns the geometry component type string, used for building component selection lists
    :param geometry: str, geometry object to query
    :return: str
    """
    check_geometry(geometry)
    geo_type = geometry_type(geometry=geometry)
    com_type = {'mesh':'vtx', 
     'nurbsSurface':'cv', 
     'nurbsCurve':'cv', 
     'lattice':'pt', 
     'particle':'pt'}
    return com_type[geo_type]


def is_a_vertex(node):
    """
    Returns whether given object is a vertex or not
    :param node: str
    :return: bool
    """
    if maya.cmds.objExists(node):
        if node.find('.vtx[') > -1:
            return True
    return False


def is_mesh_compatible(mesh1, mesh2):
    """
    Checks whether two meshes to see if they have thet same vertices, edge and face count
    :param mesh1: str
    :param mesh2: str
    :return: bool
    """
    check = MeshTopologyCheck(mesh1, mesh2)
    check_value = check.check_vert_edge_face_count()
    if not check_value:
        return False
    else:
        check_value = check.check_first_face_verts()
        return check_value


def replace(source_geometry, target_geometry):
    """
    Replaces the geometry of one object with another
    :param source_geometry: str, object that will provide the replacement geometry
    :param target_geometry: str, object whose geometry will be replaced
    """
    check_geometry(source_geometry)
    check_geometry(target_geometry)
    source_shape = source_geometry
    source_geo_type = geometry_type(source_geometry)
    if maya.cmds.objectType(source_shape) == 'transform':
        source_shapes = shape.get_shapes(source_geometry, intermediates=False)
        source_int_shapes = shape.get_shapes(source_geometry, intermediates=True)
        source_shape = source_shapes[0]
        if source_int_shapes:
            if source_geo_type == 'mesh':
                if maya.cmds.listConnections((source_shapes[0] + '.inMesh'), s=True, d=False):
                    for int_shape in source_int_shapes:
                        if maya.cmds.listConnections((int_shape + '.outMesh'), s=False, d=True):
                            source_shape = int_shape
                            break

            else:
                if source_geo_type == 'nurbsSurface' or source_geo_type == 'nurbsCurve':
                    if maya.cmds.listConnections((source_shapes[0] + '.create'), s=True, d=False):
                        for int_shape in source_int_shapes:
                            if maya.cmds.listConnections((int_shape + '.local'), s=False, d=True):
                                source_shape = int_shape
                                break

                else:
                    raise exceptions.UnknownGeometryType(source_geo_type)
        target_shape = target_geometry
        target_geo_type = geometry_type(target_geometry)
        if maya.cmds.objectType(target_shape) == 'transform':
            target_shapes = shape.get_shapes(target_geometry, intermediates=False)
            target_int_shapes = shape.get_shapes(target_geometry, intermediates=True)
            target_shape = target_int_shapes or target_shapes[0]
    else:
        if target_geo_type == 'mesh':
            if maya.cmds.listConnections((target_shapes[0] + '.inMesh'), s=True, d=False):
                for int_shape in target_int_shapes:
                    if maya.cmds.listConnections((int_shape + '.outMesh'), s=False, d=True):
                        target_shape = int_shape
                        break

        else:
            if target_geo_type == 'nurbsSurface' or target_geo_type == 'nurbsCurve':
                if maya.cmds.listConnections((target_shapes[0] + '.create'), s=True, d=False):
                    for int_shape in target_int_shapes:
                        if maya.cmds.listConnections((int_shape + '.local'), s=False, d=True):
                            target_shape = int_shape
                            break

            else:
                raise exceptions.UnknownGeometryType(target_geo_type)
    if target_geo_type != source_geo_type:
        raise Exception('Target and Source geometry types do not match! Aborting ...')
    else:
        if target_geo_type == 'mesh':
            maya.cmds.connectAttr((source_shape + '.outMesh'), (target_shape + '.inMesh'), force=True)
            maya.cmds.evalDeferred('maya.cmds.disconnectAttr("{}.outMesh", "{}.inMesh")'.format(source_shape, target_shape))
        else:
            if target_geo_type == 'nurbsSurface' or target_geo_type == 'nurbsCurve':
                maya.cmds.connectAttr((source_shape + '.local'), (target_shape + '.create'), force=True)
                maya.cmds.evalDeferred('maya.cmds.disconnectAttr("{}.local", "{}.create")'.format(source_shape, target_shape))
            else:
                raise exceptions.UnknownGeometryType(target_geo_type)


def get_mpoint_array(geometry, world_space=True):
    """
    Returns an MPointArray containing the component positions for the given geometry
    :param geometry: str, geometry to return MPointArray for
    :param world_space: bool, Whether to return point positions in world or object space
    :return: MPointArray
    """
    from tpMayaLib.core import node
    check_geometry(geometry)
    if node.get_mobject(geometry).hasFn(maya.OpenMaya.MFn.kTransform):
        try:
            geometry = maya.cmds.listRelatives(geometry, s=True, ni=True, pa=True)[0]
        except Exception:
            raise exceptions.GeometryException(geometry)

    else:
        if world_space:
            shape_obj = node.get_mdag_path(geometry)
            space = maya.OpenMaya.MSpace.kWorld
        else:
            shape_obj = node.get_mobject(geometry)
            space = maya.OpenMaya.MSpace.kObject
    shape_type = maya.cmds.objectType(geometry)
    point_list = maya.OpenMaya.MPointArray()
    if maya.is_new_api():
        if shape_type == 'mesh':
            mesh_fn = maya.OpenMaya.MFnMesh(shape_obj)
            point_list = mesh_fn.getPoints(space)
        if shape_type == 'nurbsCurve':
            curve_fn = maya.OpenMaya.MFnNurbsCurve(shape_obj)
            point_list = curve_fn.getCVs(space)
        if shape_type == 'nurbsSurface':
            surface_fn = maya.OpenMaya.MFnNurbsSurface(shape_obj)
            point_list = surface_fn.getCVs(space)
    else:
        if shape_type == 'mesh':
            mesh_fn = maya.OpenMaya.MFnMesh(shape_obj)
            mesh_fn.getPoints(point_list, space)
    if shape_type == 'nurbsCurve':
        curve_fn = maya.OpenMaya.MFnNurbsCurve(shape_obj)
        curve_fn.getCVs(point_list, space)
    if shape_type == 'nurbsSurface':
        surface_fn = maya.OpenMaya.MFnNurbsSurface(shape_obj)
        surface_fn.getCVs(point_list, space)
    return point_list


def get_point_array(geometry, world_space=True):
    """
    Returns a point array containing the component positions for the given geometry
    :param geometry: str, geometry to return point array for
    :param world_space: bool, Whether to return point positions in world or object space
    :return: list
    """
    point_array = list()
    mpoint_array = get_mpoint_array(geometry=geometry, world_space=world_space)
    mpoint_array_length = mpoint_array.length() if hasattr(mpoint_array, 'length') else len(mpoint_array)
    for i in range(mpoint_array_length):
        point_array.append([mpoint_array[i][0], mpoint_array[i][1], mpoint_array[i][2]])

    return point_array


def set_mpoint_array(geometry, points, world_space=False):
    """
    Set the points positions of a geometry node
    :param geometry: str, geometry to set points array to
    :param points: MPointArray, point array of points
    :param world_space:
    :return: bool, Whether to set point positions in world or object space
    """
    from tpMayaLib.core import node
    check_geometry(geometry)
    if world_space:
        shape_obj = node.get_mdag_path(geometry)
        space = maya.OpenMaya.MSpace.kWorld
    else:
        shape_obj = node.get_mobject(geometry)
        space = maya.OpenMaya.MSpace.kObject
    it_geo = maya.OpenMaya.MItGeometry(shape_obj)
    it_geo.setAllPositions(points, space)


def get_mbounding_box(geometry, world_space=True):
    """
    Returns an MBoundingBox for the given geometry
    :param geometry: str, geometry to return MBoundingBox for
    :param world_space: bool, Whether to calculate MBoundingBox in world or object space
    :return: MBoundingBox
    """
    from tpMayaLib.core import node
    check_geometry(geometry)
    geo_path = node.get_mdag_path(geometry)
    geo_node_fn = maya.OpenMaya.MFnDagNode(geo_path)
    geo_bbox = geo_node_fn.boundingBox()
    if world_space:
        geo_bbox.transformUsing(geo_path.exclusiveMatrix())
    else:
        LOGGER.warning('Local space Bounding Bosx is not fully reliable ...')
        geo_bbox.transformUsing(geo_node_fn.transformationMatrix().inverse())
    return geo_bbox


def smooth_preview(geometry, smooth_flag=True):
    """
    Turns on/off smooth preview of the given geometry node
    :param geometry: str, name of the geometry to set smooth preview
    :param smooth_flag: bool
    """
    if smooth_flag:
        maya.cmds.setAttr('{}.displaySmoothMesh'.format(geometry), 2)
    else:
        maya.cmds.setAttr('{}.displaySmoothMesh'.format(geometry), 0)


def smooth_preview_all(smooth_flag=True):
    """
    Turns on/off smooth preview of all the meshes in the current scene
    :param smooth_flag: bool
    """
    from tpMayaLib.core import scene
    if scene.is_batch():
        return
    meshes = maya.cmds.ls(type='mesh')
    for mesh in meshes:
        intermediate = maya.cmds.getAttr('{}.intermediateObject'.format(mesh))
        if not intermediate:
            smooth_preview(mesh, smooth_flag)


def transforms_to_nurbs_surface(transforms, name, spans=-1, offset_axis='Y', offset_amount=1):
    """
    Creates a NURBS surface from a list of transforms
    Useful for creating a NURBS surface that follows a spine or tail
    :param transforms: list<str>, list of transforms
    :param name: str, name of the surface
    :param spans: int, number of spans to given to the final surface.
    If -1, the surface will have spans based on the number of transforms
    :param offset_axis: str, axis to offset the surface relative to the transform ('X', 'Y' or 'Z')
    :param offset_amount: int, amount the surface offsets from the transform
    :return: str, name of the NURBS surface
    """
    transform_positions_1 = list()
    transform_positions_2 = list()
    if offset_axis == 0:
        offset_axis = 'X'
    else:
        if offset_axis == 1:
            offset_axis = 'Y'
        else:
            if offset_axis == 2:
                offset_axis = 'Z'
    for xform in transforms:
        xform_1 = maya.cmds.group(empty=True)
        xform_2 = maya.cmds.group(empty=True)
        xform_utils.MatchTransform(xform, xform_1).translation_rotation()
        xform_utils.MatchTransform(xform, xform_2).translation_rotation()
        vct = mathlib.get_axis_vector(offset_axis)
        maya.cmds.move((vct[0] * offset_amount), (vct[1] * offset_amount), (vct[2] * offset_amount), xform_1, relative=True, os=True)
        maya.cmds.move((vct[0] * -offset_amount), (vct[1] * -offset_amount), (vct[2] * -offset_amount), xform_2, relative=True, os=True)
        pos_1 = maya.cmds.xform(xform_1, q=True, ws=True, t=True)
        pos_2 = maya.cmds.xform(xform_2, q=True, ws=True, t=True)
        transform_positions_1.append(pos_1)
        transform_positions_2.append(pos_2)
        maya.cmds.delete(xform_1, xform_2)

    crv_1 = maya.cmds.curve(p=transform_positions_1, degree=1)
    crv_2 = maya.cmds.curve(p=transform_positions_2, degree=1)
    crvs = [crv_1, crv_2]
    if not spans == -1:
        for crv in crvs:
            maya.cmds.rebuildCurve(crv, ch=False, rpo=True, rt=0, end=1, kr=False, kcp=False, kep=True, kt=False, spans=spans, degree=3, tol=0.01)

    loft = maya.cmds.loft(crv_1, crv_2, n=(name_utils.find_unique_name(name)), ss=1, degree=1, ch=False)
    maya.cmds.delete(crv_1, crv_2)
    return loft[0]


def get_mesh_shape(mesh, shape_index=0):
    """
    Returns the first mesh shape or one based in the index
    :param mesh: str, name of a mesh
    :param shape_index: int, index of shape to retrieve (usually is 0)
    :return: str, name of the shape. If no mesh shapes found then returns None
    """
    if mesh.find('.vtx'):
        mesh = mesh.split('.')[0]
    else:
        if maya.cmds.nodeType(mesh) == 'mesh':
            mesh = maya.cmds.listRelatives(mesh, p=True, f=True)[0]
        shapes = shape.get_shapes_of_type(mesh)
        if not shapes:
            return
        else:
            return maya.cmds.nodeType(shapes[0]) == 'mesh' or None
    shape_count = len(shapes)
    if shape_index < shape_count:
        return shapes[0]
    else:
        if shape_index > shape_count:
            LOGGER.warning('{} does not have a shape count up to {}'.format(mesh, shape_index))
            return
        return shapes[shape_index]


def get_vertices(geo_obj):
    """
    Returns list of vertices of the given geometry
    :param geo_obj: str, name of the geometry
    :return: list<str>
    """
    mesh = get_mesh_shape(geo_obj)
    meshes = shape.get_shapes_of_type(mesh, 'mesh', no_intermediate=True)
    found = list()
    for mesh in meshes:
        verts = maya.cmds.ls(('{}.vtx[*]'.format(mesh)), flatten=True)
        if verts:
            found += verts

    return found


def get_faces(geo_obj):
    """
    Returns list of faces of the given geometry
    :param geo_obj: str, name of the geometry
    :return: list<str>
    """
    mesh = get_mesh_shape(geo_obj)
    meshes = shape.get_shapes_of_type(mesh, 'mesh', no_intermediate=True)
    found = list()
    for mesh in meshes:
        faces = maya.cmds.ls(('{}.f[*]'.format(mesh)), flatten=True)
        if faces:
            found += faces

    return found


def get_vertex_indices(list_of_vertex_names):
    """
    Returns list of indices of the given vertices
    :param list_of_vertex_names: list<str>
    :return: list<int>
    """
    list_of_vertex_names = python.force_list(list_of_vertex_names)
    vertex_indices = list()
    for vertex in list_of_vertex_names:
        index = int(vertex[vertex.find('[') + 1:vertex.find(']')])
        vertex_indices.append(index)

    return vertex_indices


def faces_to_vertices(faces):
    """
    Converts given faces to vertices
    :param faces: list<str>
    :return: list<str>
    """
    faces = maya.cmds.ls(faces, flatten=True)
    verts = list()
    mesh = faces[0].split('.')[0]
    for face in faces:
        info = maya.cmds.polyInfo(face, faceToVertex=True)[0].split()
        sub_verts = info[2:]
        for sub_vert in sub_verts:
            if sub_vert not in verts:
                verts.append('{}.vtx[{}]'.format(mesh, sub_vert))

    return verts


def get_closest_parameter_on_surface(surface, vector):
    """
    Returns the closest parameter value on the surface given vector
    :param surface: str, name of the surface
    :param vector: list(float, float, float(, position from which to check for closes parameter on surface
    :return: list(int, int), parameter coordinates (UV) of the closest point on the surface
    """
    shapes = shape.get_shapes(surface)
    surface = shapes[0] if shapes else surface
    surface = api.NurbsSurfaceFunction(surface)
    uv = surface.get_closest_parameter(vector)
    uv = list(uv)
    if uv[0] == 0:
        uv[0] = 0.001
    if uv[1] == 0:
        uv[1] = 0.001
    return uv


def get_closest_normal_on_surface(surface, vector):
    """
    Returns the closest normal on the surface given vector
    :param surface: str, name of the surface
    :param vector:
    :return:
    """
    shapes = shape.get_shapes(surface)
    surface = shapes[0] if shapes else surface
    surface = api.NurbsSurfaceFunction(surface)
    return surface.get_closest_normal(vector)


def get_point_from_surface_parameter(surface, u_value, v_value):
    """
    Returns surface point in given UV values
    :param surface: str, name of a surface
    :param u_value: int, u value
    :param v_value: int, v value
    :return: float(list, list, list)
    """
    surface_fn = api.NurbsSurfaceFunction(surface)
    position = surface_fn.get_position_from_parameter(u_value, v_value)
    return position