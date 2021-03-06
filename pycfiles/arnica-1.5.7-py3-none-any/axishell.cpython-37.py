# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/duranton/Documents/CERFACS/CODES/arnica/src/arnica/utils/axishell.py
# Compiled at: 2020-03-30 05:30:51
# Size of source mod 2**32: 12318 bytes
""" axishell module
to create x-axisymmetric shells for scientific computations
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import json, numpy as np
from scipy import interpolate, spatial
MESH_CTRL_POINTS = 'axishell.json'
MAX_SPLINE_ORDER = 3
SPLINE_SMOOTHNESS = 0
MATRIX_ELEMENTS = [
 'xyz', 'r', 'theta',
 'n_x', 'n_y', 'n_z', 'n_r']
AXIS_NAMES = ['time', 'theta', 'r']

class AxiShell:
    __doc__ = '\\\n    *Base class for x-axisymmetric computationnal shells*\n\n    ::\n    \n                ___________\n         ___----           ----___     Cylindrical system\n        \\                         /    Example angle = 0 deg\n         \\                       /\n          \\                     /      r - longi\n           \\                   /       ^\n            \\                 /        |\n             \\      ___      /         |\n              \\__---   ---__/          X-----> theta - azi\n                                      x\n\n\n    :param n_longi: Number of longitudinal cut points\n    :type n_longi: int\n    :param n_azi: Number of azimuthal cut points\n    :type n_azi: int\n\n    :param shape: Number of cut points n_longi and n_azi\n    :type shape: tuple of int(dim 2)\n    :param geom: dict() containing the geometrical parameters :\n\n        - **angle**      - float - Axi-symmetric angle range\n        - **angle_min**  - float - Minimum axi-symmetric angle\n        - **ctrl_pts_x** - tuple of float - x-component of the spline control point\n        - **ctrl_pts_r** - tuple of float - r-component of the spline control point\n    :param matrix: dict() containing shell data :\n\n        - **xyz**   - np.array of dim (n_azi,n_longi,3) - Array of x,y,z-components\n        - **r**     - np.array of dim (n_azi,n_longi) - Array of r-component\n        - **theta** - np.array of dim (n_azi,n_longi) - Array of theta-component\n        - **n_x**   - np.array of dim (n_azi,n_longi) - Array of normal x-component\n        - **n_y**   - np.array of dim (n_azi,n_longi) - Array of normal y-component\n        - **n_z**   - np.array of dim (n_azi,n_longi) - Array of normal z-component\n        - **n_r**   - np.array of dim (n_azi,n_longi) - Array of normal r-component\n\n    :param cake: dict() containing 3D mesh from 2D shell extrusion :\n\n        - *xyz* - np.array of dim (n_azi, n_longi, n_layers, 3) - Array of x,y,z-components\n        - *dz*  - np.array of dim (n_azi, n_longi, n_layers) - Array of width per layer\n\n    '

    def __init__(self, n_longi, n_azi):
        """
        *Initialize an AxiShell object*
        """
        self.shape = (
         n_azi, n_longi)
        self.geom = {}
        self.matrix = {}
        self.cake = {}

    def init_mockup(self):
        """
        *Initialize with a mockup mesh*
        """
        self.geom['angle'] = 40.0
        self.geom['crtl_pts_x'] = (0.0, 0.2)
        self.geom['crtl_pts_r'] = (0.12, 0.12)
        self.build_shell()

    def load(self):
        """
        *Load AxiShell geometric features in JavaScript Object Notation*
        """
        with open(MESH_CTRL_POINTS, 'r') as (fin):
            self.geom = json.load(fin)
        self.build_shell()

    def dump(self):
        """
        *Dump AxiShell geometric features in JavaScript Object Notation*
        """
        with open(MESH_CTRL_POINTS, 'w') as (fout):
            json.dump(self.geom, fout)

    def build_shell(self):
        """
        *Build shell from geometric features*

            - Construct a spline used as base for extrusion              from control points : tck
            - Discretise the spline : shell_crest
            - Compute normal vectors for the 1D shell_crest
            - Compute r,n_x,n_r-components for 2D shell
            - Compute theta-components for 2D shell
            - Compute xyz,n_y,n_z-components for 2D shell
        """
        spline_order = min(len(self.geom['crtl_pts_x']) - 1, MAX_SPLINE_ORDER)
        tck, _ = interpolate.splprep([self.geom['crtl_pts_x'],
         self.geom['crtl_pts_r']],
          s=SPLINE_SMOOTHNESS,
          k=spline_order)
        unew = np.linspace(0, 1,
          num=(self.shape[1]))
        shell_crest = np.asarray(interpolate.splev(unew, tck))
        normal_vects = np.roll((np.diff(shell_crest)), 1, axis=0)
        normal_vects /= np.linalg.norm(normal_vects, axis=0)
        normal_vects[0, :] *= -1
        normal_vects2 = np.ones((2, self.shape[1]))
        normal_vects2[:, :self.shape[1] - 1] = normal_vects
        normal_vects2[:, -1] = normal_vects[:, -1]
        for item in MATRIX_ELEMENTS:
            self.matrix[item] = np.ones(self.shape)

        tmp_x = np.tile(shell_crest[0], (self.shape[0], 1))
        self.matrix['r'] = np.tile(shell_crest[1], (self.shape[0], 1))
        self.matrix['n_x'] = np.tile(normal_vects2[0], (self.shape[0], 1))
        self.matrix['n_r'] = np.tile(normal_vects2[1], (self.shape[0], 1))
        rot_angle = 0
        if 'angle_min' in self.geom:
            rot_angle = 0.5 * self.geom['angle'] + self.geom['angle_min']
        min_theta = (rot_angle - 0.5 * self.geom['angle']) * np.pi / 180
        max_theta = (rot_angle + 0.5 * self.geom['angle']) * np.pi / 180
        self.matrix['theta'] = np.transpose(np.tile(np.linspace(min_theta, max_theta, num=(self.shape[0])), (
         self.shape[1], 1)))
        tmp_y = self.matrix['r'] * np.cos(self.matrix['theta'])
        tmp_z = self.matrix['r'] * np.sin(self.matrix['theta'])
        self.matrix['xyz'] = np.stack((tmp_x, tmp_y, tmp_z), axis=2)
        self.matrix['n_y'] = self.matrix['n_r'] * np.cos(self.matrix['theta'])
        self.matrix['n_z'] = self.matrix['n_r'] * np.sin(self.matrix['theta'])

    def add_curviwidth(self, label, points):
        """
        *Add a 2D width matrix of shell shape extruded from points spline*

        :param label: Label of the width matrix
        :type label: str
        :param points: Tuple (dim n) of tuple (dim 2) of float coordinates        """
        x_tuple, y_tuple = tuple(zip(*points))
        xlist = [
         0] + list(x_tuple) + [1]
        ylist = [y_tuple[0]] + list(y_tuple) + [y_tuple[(-1)]]
        f_int = interpolate.interp1d(xlist, ylist)
        xnew = np.linspace(0, 1, num=(self.shape[1]))
        ynew = f_int(xnew)
        self.matrix[label] = np.tile(ynew, (self.shape[0], 1))

    def set_mask_on_shell(self, point_cloud, tol):
        """
        *Create a mask on the shell from a point cloud*

        The mask value is 1 for shell points located near cloud points.

        :param point_cloud: Array of dim (n,3) of coordinates of points.
        :type point_cloud: numpy array
        :param tol: Tolerance of proximity
        :type tol: int
        """
        kdtree = spatial.KDTree(point_cloud)
        dists, _ = kdtree.query((self.matrix['xyz']), k=1)
        self.matrix['mask'] = np.where(dists.reshape(self.shape) > tol, np.zeros(self.shape), np.ones(self.shape))

    def bake_millefeuille(self, width_matrix_label, n_layers, shift=0.0):
        """
        *Create a millefeuille-like shell.*

        Extrude a 2D shell in the normal direction up
        pointwise height given by "width_matrix_label" matrix.

        :param width_matrix_label: Label of the width matrix
        :type width_matrix_label: str
        :param n_layers: Number of layer for extrusion
        :type n_layers: int
        :param shift: Additional depth (optional)
        :type shift: float

        :returns:

            - **cake** - A dict() containing shell data :

                - *xyz* - np.array of dim (n_longi, n_azi, n_layers, 3)
                - *dz*  - np.array of dim (n_longi, n_azi, n_layers)

        "Bon appetit!"
        """
        cake = {}
        cake['xyz'] = np.empty((self.shape[0],
         self.shape[1],
         n_layers,
         3))
        cake['dz'] = np.empty((self.shape[0],
         self.shape[1],
         n_layers))
        for j, dim in enumerate(['x', 'y', 'z']):
            for i in range(n_layers):
                cake['xyz'][:, :, i, j] = self.matrix['xyz'][:, :, j] + (1.0 * i / n_layers * self.matrix[width_matrix_label] + shift) * self.matrix[('n_' + dim)]

        for i in range(n_layers):
            cake['dz'][:, :, i] = abs(self.matrix[width_matrix_label] / n_layers)

        cake['dz'][:, :, 0] /= 2
        cake['dz'][:, :, -1] /= 2
        return cake

    def average_on_shell_over_dirs(self, variable, directions):
        """
        *Performs an integration (averaging) over one or multiple directions*

        :param variable: A np.array to be averaged of dim (n_time, n_theta, n_r)
        :param directions: A list() of directions on which the average process                           is to be performed.                           Contains keywords from ['time','theta','r'].

        :returns:

            - **averaged_variable** - A np.array of averaged data on given directions.
        """
        scaled = np.copy(variable)
        if self.matrix.get('surf') is not None:
            scaled = np.multiply(variable, self.matrix.get('surf'))
        dirs = AXIS_NAMES.copy()
        if len(directions) > 0 and all((dir_ in dirs for dir_ in directions)):
            averaged_variable = scaled
            for dir_ in directions:
                index = dirs.index(dir_)
                averaged_variable = np.mean(averaged_variable, axis=index)
                dirs.pop(index)

        else:
            mess = 'Averaging directions do not conform to criteria\n'
            mess += 'It should be a list containing one of or all items\n'
            mess += '"time", "theta", "r"'
            raise ValueError(mess)
        return averaged_variable


def width_mockup():
    """ Create a mockup tuple of tuple for widths"""
    width_mockup_ = ((0.0, -0.04), (0.2, -0.04), (0.3, -0.07), (0.4, -0.07), (0.5, -0.04),
                     (0.8, -0.04))
    return width_mockup_