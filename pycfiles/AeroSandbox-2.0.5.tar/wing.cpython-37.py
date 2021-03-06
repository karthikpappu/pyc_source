# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Projects\GitHub\AeroSandbox\aerosandbox\geometry\wing.py
# Compiled at: 2020-04-22 19:36:48
# Size of source mod 2**32: 13020 bytes
from aerosandbox.geometry.common import *

class Wing(AeroSandboxObject):
    __doc__ = '\n    Definition for a wing.\n    If the wing is symmetric across the XZ plane, just define the right half and supply "symmetric = True" in the constructor.\n    If the wing is not symmetric across the XZ plane, just define the wing.\n    '

    def __init__(self, name='Untitled Wing', x_le=0, y_le=0, z_le=0, xsecs=[], symmetric=False, chordwise_panels=8, chordwise_spacing='cosine'):
        self.name = name
        self.xyz_le = cas.vertcat(x_le, y_le, z_le)
        self.xsecs = xsecs
        self.symmetric = symmetric
        self.chordwise_panels = chordwise_panels
        self.chordwise_spacing = chordwise_spacing

    def __repr__(self):
        return 'Wing %s (%i xsecs, %s)' % (
         self.name,
         len(self.xsecs),
         'symmetric' if self.symmetric else 'not symmetric')

    def area(self, type='wetted'):
        """
        Returns the area, with options for various ways of measuring this.
         * wetted: wetted area
         * projected: area projected onto the XY plane (top-down view)
        :param type:
        :return:
        """
        area = 0
        for i in range(len(self.xsecs) - 1):
            chord_eff = (self.xsecs[i].chord + self.xsecs[(i + 1)].chord) / 2
            this_xyz_te = self.xsecs[i].xyz_te()
            that_xyz_te = self.xsecs[(i + 1)].xyz_te()
            if type == 'wetted':
                span_le_eff = cas.sqrt((self.xsecs[i].xyz_le[1] - self.xsecs[(i + 1)].xyz_le[1]) ** 2 + (self.xsecs[i].xyz_le[2] - self.xsecs[(i + 1)].xyz_le[2]) ** 2)
                span_te_eff = cas.sqrt((this_xyz_te[1] - that_xyz_te[1]) ** 2 + (this_xyz_te[2] - that_xyz_te[2]) ** 2)
            else:
                if type == 'projected':
                    span_le_eff = cas.fabs(self.xsecs[i].xyz_le[1] - self.xsecs[(i + 1)].xyz_le[1])
                    span_te_eff = cas.fabs(this_xyz_te[1] - that_xyz_te[1])
                else:
                    raise ValueError("Bad value of 'type'!")
            span_eff = (span_le_eff + span_te_eff) / 2
            area += chord_eff * span_eff

        if self.symmetric:
            area *= 2
        return area

    def span(self, type='wetted'):
        """
        Returns the span, with options for various ways of measuring this.
         * wetted: Adds up YZ-distances of each section piece by piece
         * yz: YZ-distance between the root and tip of the wing
         * y: Y-distance between the root and tip of the wing
         * z: Z-distance between the root and tip of the wing
        If symmetric, this is doubled to obtain the full span.
        :param type: One of the above options, as a string.
        :return: span
        """
        if type == 'wetted':
            span = 0
            for i in range(len(self.xsecs) - 1):
                sect1_xyz_le = self.xsecs[i].xyz_le
                sect2_xyz_le = self.xsecs[(i + 1)].xyz_le
                sect1_xyz_te = self.xsecs[i].xyz_te()
                sect2_xyz_te = self.xsecs[(i + 1)].xyz_te()
                span_le = cas.sqrt((sect1_xyz_le[1] - sect2_xyz_le[1]) ** 2 + (sect1_xyz_le[2] - sect2_xyz_le[2]) ** 2)
                span_te = cas.sqrt((sect1_xyz_te[1] - sect2_xyz_te[1]) ** 2 + (sect1_xyz_te[2] - sect2_xyz_te[2]) ** 2)
                span_eff = (span_le + span_te) / 2
                span += span_eff

        else:
            if type == 'yz':
                root = self.xsecs[0]
                tip = self.xsecs[(-1)]
                span = cas.sqrt((root.xyz_le[1] - tip.xyz_le[1]) ** 2 + (root.xyz_le[2] - tip.xyz_le[2]) ** 2)
            else:
                if type == 'y':
                    root = self.xsecs[0]
                    tip = self.xsecs[(-1)]
                    span = cas.fabs(tip.xyz_le[1] - root.xyz_le[1])
                else:
                    if type == 'z':
                        root = self.xsecs[0]
                        tip = self.xsecs[(-1)]
                        span = cas.fabs(tip.xyz_le[2] - root.xyz_le[2])
                    else:
                        raise ValueError("Bad value of 'type'!")
        if self.symmetric:
            span *= 2
        return span

    def aspect_ratio(self):
        return self.span() ** 2 / self.area()

    def has_symmetric_control_surfaces(self):
        for xsec in self.xsecs:
            if not xsec.control_surface_type == 'symmetric':
                return False

        return True

    def mean_geometric_chord(self):
        """
        Returns the mean geometric chord of the wing (S/b).
        :return:
        """
        return self.area() / self.span()

    def mean_twist_angle(self):
        r"""
        Returns the mean twist angle (in degrees) of the wing, weighted by span.
        You can think of it as \int_{b}(twist)db, where b is span.
        WARNING: This function's output is only exact in the case where all of the cross sections have the same twist axis!
        :return: mean twist angle (in degrees)
        """
        span = []
        for i in range(len(self.xsecs) - 1):
            sect1_xyz_le = self.xsecs[i].xyz_le
            sect2_xyz_le = self.xsecs[(i + 1)].xyz_le
            sect1_xyz_te = self.xsecs[i].xyz_te()
            sect2_xyz_te = self.xsecs[(i + 1)].xyz_te()
            span_le = cas.sqrt((sect1_xyz_le[1] - sect2_xyz_le[1]) ** 2 + (sect1_xyz_le[2] - sect2_xyz_le[2]) ** 2)
            span_te = cas.sqrt((sect1_xyz_te[1] - sect2_xyz_te[1]) ** 2 + (sect1_xyz_te[2] - sect2_xyz_te[2]) ** 2)
            span_eff = (span_le + span_te) / 2
            span.append(span_eff)

        twist_span_product = 0
        for i in range(len(self.xsecs)):
            xsec = self.xsecs[i]
            if i > 0:
                twist_span_product += xsec.twist * span[(i - 1)] / 2
            if i < len(self.xsecs) - 1:
                twist_span_product += xsec.twist * span[i] / 2

        mean_twist = twist_span_product / cas.sum1((cas.vertcat)(*span))
        return mean_twist

    def mean_sweep_angle(self):
        """
        Returns the mean quarter-chord sweep angle (in degrees) of the wing, relative to the x-axis.
        Positive sweep is backwards, negative sweep is forward.
        :return:
        """
        root_quarter_chord = 0.75 * self.xsecs[0].xyz_le + 0.25 * self.xsecs[0].xyz_te()
        tip_quarter_chord = 0.75 * self.xsecs[(-1)].xyz_le + 0.25 * self.xsecs[(-1)].xyz_te()
        vec = tip_quarter_chord - root_quarter_chord
        vec_norm = vec / cas.norm_2(vec)
        sin_sweep = vec_norm[0]
        sweep_deg = cas.asin(sin_sweep) * 180 / cas.pi
        return sweep_deg

    def approximate_center_of_pressure(self):
        """
        Returns the approximate location of the center of pressure. Given as the area-weighted quarter chord of the wing.
        :return: [x, y, z] of the approximate center of pressure
        """
        areas = []
        quarter_chord_centroids = []
        for i in range(len(self.xsecs) - 1):
            chord_eff = (self.xsecs[i].chord + self.xsecs[(i + 1)].chord) / 2
            this_xyz_te = self.xsecs[i].xyz_te()
            that_xyz_te = self.xsecs[(i + 1)].xyz_te()
            span_le_eff = cas.sqrt((self.xsecs[i].xyz_le[1] - self.xsecs[(i + 1)].xyz_le[1]) ** 2 + (self.xsecs[i].xyz_le[2] - self.xsecs[(i + 1)].xyz_le[2]) ** 2)
            span_te_eff = cas.sqrt((this_xyz_te[1] - that_xyz_te[1]) ** 2 + (this_xyz_te[2] - that_xyz_te[2]) ** 2)
            span_eff = (span_le_eff + span_te_eff) / 2
            areas.append(chord_eff * span_eff)
            quarter_chord_centroids.append((0.75 * self.xsecs[i].xyz_le + 0.25 * self.xsecs[i].xyz_te() + 0.75 * self.xsecs[(i + 1)].xyz_le + 0.25 * self.xsecs[(i + 1)].xyz_te()) / 2 + self.xyz_le)

        areas = (cas.vertcat)(*areas)
        quarter_chord_centroids = cas.transpose((cas.horzcat)(*quarter_chord_centroids))
        total_area = cas.sum1(areas)
        approximate_cop = cas.sum1(areas / cas.sum1(areas) * quarter_chord_centroids)
        if self.symmetric:
            approximate_cop[:, 1] = 0
        return approximate_cop


class WingXSec(AeroSandboxObject):
    __doc__ = '\n    Definition for a wing cross section ("X-section").\n    '

    def __init__(self, x_le=0, y_le=0, z_le=0, chord=0, twist=0, twist_axis=cas.DM([0, 1, 0]), airfoil=None, control_surface_type='symmetric', control_surface_hinge_point=0.75, control_surface_deflection=0, spanwise_panels=8, spanwise_spacing='cosine'):
        if airfoil is None:
            raise ValueError("'airfoil' argument missing! (Needs an object of Airfoil type)")
        self.x_le = x_le
        self.y_le = y_le
        self.z_le = z_le
        self.chord = chord
        self.twist = twist
        self.twist_axis = twist_axis
        self.airfoil = airfoil
        self.control_surface_type = control_surface_type
        self.control_surface_hinge_point = control_surface_hinge_point
        self.control_surface_deflection = control_surface_deflection
        self.spanwise_panels = spanwise_panels
        self.spanwise_spacing = spanwise_spacing
        self.xyz_le = cas.vertcat(x_le, y_le, z_le)

    def __repr__(self):
        return 'WingXSec (airfoil = %s, chord = %f, twist = %f)' % (
         self.airfoil.name,
         self.chord,
         self.twist)

    def xyz_te(self):
        rot = angle_axis_rotation_matrix(self.twist * cas.pi / 180, self.twist_axis)
        xyz_te = self.xyz_le + rot @ cas.vertcat(self.chord, 0, 0)
        return xyz_te