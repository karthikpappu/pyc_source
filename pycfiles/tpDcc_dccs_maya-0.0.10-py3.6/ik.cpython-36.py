# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpDcc/dccs/maya/core/ik.py
# Compiled at: 2020-05-13 19:28:33
# Size of source mod 2**32: 11536 bytes
"""
Module that contains functions and classes related with IKs
"""
from __future__ import print_function, division, absolute_import
import tpDcc as tp
from tpDcc.libs.python import mathlib
import tpDcc.dccs.maya as maya
from tpDcc.dccs.maya.core import attribute as attr_utils

class IkHandle(object):
    __doc__ = '\n    Base class to crete and work with IK handles\n    '
    SOLVER_RP = 'ikRPsolver'
    SOLVER_SC = 'ikSCsolver'
    SOLVER_SPLINE = 'ikSplineSolver'
    SOLVER_SPRING = 'ikSpringSolver'

    def __init__(self, name):
        self._name = name
        self._start_joint = None
        self._end_joint = None
        self._solver_type = self.SOLVER_SC
        self._curve = None
        self._ik_handle = None
        self._ik_effector = None
        self._joints = list()

    def set_start_joint(self, joint):
        """
        Set start joint for IK handle to use
        :param joint: str, name of the start joint
        """
        self._start_joint = joint

    def set_end_joint(self, joint):
        """
        Set end joint for IK handle to use
        :param joint: str, name of the end joint
        """
        self._end_joint = joint

    def set_joints(self, joints_list):
        """
        Sets  the ojints for the IK handle to use
        First entry of the list is the start joint and the last entry is the end joint
        :param joints_list: list<str>, a list of joints
        """
        self._start_joint = joints_list[0]
        self._end_joint = joints_list[(-1)]
        self._joints = joints_list

    def set_curve(self, curve):
        """
        Sets teh curve for Spline IK handle to use
        :param curve: str, name of the curve
        """
        if type(curve) in [list, tuple]:
            self._curve = curve[0]
        else:
            self._curve = curve

    def set_solver(self, solver_name):
        """
        Sets the solver type for the IK handle to use
        :param solver_name: str, name of the solver type to use:
            'ikRPsolver'
            'ikSCsolver'
            'ikSplineSolver'
            'ikSpringSolver'
        """
        self._solver_type = solver_name

    def set_full_name(self, full_name):
        """
        Sets the full name for the IK handle to use
        :param full_name: str
        """
        self._name = full_name

    def create(self):
        """
        Creates IK handle with the store atrributes
        :return: str, name of thre IK handle
        """
        if not self._start_joint or not self._end_joint:
            return
        else:
            if not self._curve:
                if not self._solver_type == self.SOLVER_SPLINE:
                    self._create_regular_ik()
            if self._curve or self._solver_type == self.SOLVER_SPLINE:
                self._solver_type = self.SOLVER_SPLINE
                self._create_spline_ik()
            return self._ik_handle

    def _create_regular_ik(self):
        ik_handle, ik_effector = maya.cmds.ikHandle(name=(tp.Dcc.find_unique_name(self._name)),
          startJoint=(self._start_joint),
          endEffector=(self._end_joint),
          sol=(self._solver_type))
        maya.cmds.rename(ik_effector, tp.Dcc.find_unique_name('effector_{}'.format(ik_handle)))
        self._ik_handle = ik_handle
        self._ik_effector = ik_effector

    def _create_spline_ik(self):
        if self._curve:
            ik_handle = maya.cmds.ikHandle(name=(tp.Dcc.find_unique_name(self._name)),
              startJoint=(self._start_joint),
              endEffector=(self._end_joint),
              sol=(self._solver_type),
              curve=(self._curve),
              ccv=False,
              pcv=False)
            maya.cmds.rename(ik_handle[1], 'effector_{}'.format(ik_handle[0]))
            self._ik_handle = ik_handle[0]
            self._ik_effector = ik_handle[1]
        else:
            ik_handle = maya.cmds.ikHandle(name=(tp.Dcc.find_unique_name(self._name)),
              startJoint=(self._start_joint),
              endEffector=(self._end_joint),
              sol=(self._solver_type),
              scv=False,
              pcv=False)
            maya.cmds.rename(ik_handle[1], 'effector_{}'.format(ik_handle[0]))
            self._ik_handle = ik_handle[0]
            self._ik_effector = ik_handle[1]
            self._curve = ik_handle[2]
            self._curve = maya.cmds.rename(self._curve, tp.Dcc.find_unique_name('curve_{}'.format(self._name)))


def create_spline_ik_stretch(curve, joints, node_for_attribute=None, create_stretch_on_off=False, create_bulge=True, scale_axis='X'):
    """
    Makes the joints stretch on the curve
    :param curve: str, name of the curve that joints are attached via Spline IK
    :param joints: list<str>, list of joints attached to Spline IK
    :param node_for_attribute: str, name of the node to create the attributes on
    :param create_stretch_on_off: bool, Whether to create or not extra attributes to slide the stretch value on/off
    :param create_bulge: bool, Whether to add bulging to the other axis that are not the scale axis
    :param scale_axis: str('X', 'Y', 'Z'), axis that the joints stretch on
    """
    if scale_axis == 0:
        scale_axis = 'X'
    else:
        if scale_axis == 1:
            scale_axis = 'Y'
        else:
            if scale_axis == 2:
                scale_axis = 'Z'
            else:
                scale_axis = scale_axis.capitalize()
    name = 'curveInfo_{}'.format(curve)
    arclen_node = maya.cmds.arclen(curve, ch=True, n=(tp.Dcc.find_unique_name(name)))
    arclen_node = maya.cmds.rename(arclen_node, tp.Dcc.find_unique_name(name))
    name1 = 'multiplyDivide_offset_{}'.format(arclen_node)
    name2 = 'multiplyDivide_{}'.format(arclen_node)
    multiply_scale_offset = maya.cmds.createNode('multiplyDivide', n=(tp.Dcc.find_unique_name(name1)))
    multiply = maya.cmds.createNode('multiplyDivide', n=(tp.Dcc.find_unique_name(name2)))
    maya.cmds.setAttr('{}.operation'.format(multiply_scale_offset), 2)
    maya.cmds.connectAttr('{}.arcLength'.format(arclen_node), '{}.input1X'.format(multiply_scale_offset))
    maya.cmds.connectAttr('{}.outputX'.format(multiply_scale_offset), '{}.input1X'.format(multiply))
    maya.cmds.setAttr('{}.input2X'.format(multiply), maya.cmds.getAttr('{}.arcLength'.format(arclen_node)))
    maya.cmds.setAttr('{}.operation'.format(multiply), 2)
    joint_count = len(joints)
    segment = 1.0 / joint_count
    percent = 0
    for jnt in joints:
        mult_attr = '{}.outputX'.format(multiply)
        if create_stretch_on_off:
            if node_for_attribute:
                attr = attr_utils.NumericAttribute('stretchOnOff')
                attr.set_min_value(0)
                attr.set_max_value(1)
                attr.set_keyable(True)
                attr.create(node_for_attribute)
                blend_name = 'blendColors_stretchOnOff_{}'.format(curve)
                blend = maya.cmds.createNode('blendColors', n=blend_name)
                maya.cmds.connectAttr(mult_attr, '{}.color1R'.format(blend))
                maya.cmds.setAttr('{}.color2R'.format(blend), 1)
                maya.cmds.connectAttr('{}.outputR'.format(blend), '{}.scale{}'.format(jnt, scale_axis))
                maya.cmds.connectAttr('{}.stretchOnOff'.format(node_for_attribute), '{}.blender'.format(blend))
        if not create_stretch_on_off:
            maya.cmds.connectAttr(mult_attr, '{}.scale{}'.format(jnt, scale_axis))
        if create_bulge:
            plus_name = 'plusMinusAverage_bulge_scale_{}'.format(jnt)
            plus = maya.cmds.createNode('plusMinusAverage', n=plus_name)
            maya.cmds.addAttr(plus, ln='scaleOffset', dv=1, k=True)
            maya.cmds.addAttr(plus, ln='bulge', dv=1, k=True)
            arc_value = mathlib.fade_sine(percent)
            attr_utils.connect_multiply('{}.outputX'.format(multiply_scale_offset), '{}.bulge'.format(plus), arc_value)
            attr_utils.connect_plus('{}.scaleOffset'.format(plus), '{}.input1D[0]'.format(plus))
            attr_utils.connect_plus('{}.bulge'.format(plus), '{}.input1D[1]'.format(plus))
            scale_value = maya.cmds.getAttr('{}.output1D'.format(plus))
            mult_offset_name = 'multiply_{}'.format(jnt)
            multiply_offset = maya.cmds.createNode('multiplyDivide', n=mult_offset_name)
            maya.cmds.setAttr('{}.operation'.format(multiply_offset), 2)
            maya.cmds.setAttr('{}.input1X'.format(multiply_offset), scale_value)
            maya.cmds.connectAttr('{}.output1D'.format(plus), '{}.input2X'.format(multiply_offset))
            blend_name = 'blendColors_{}'.format(jnt)
            blend = maya.cmds.createNode('blendColors', n=blend_name)
            blend_attr = '{}.outputR'.format(blend)
            if node_for_attribute:
                maya.cmds.connectAttr('{}.outputX'.format(multiply_offset), '{}.color1R'.format(blend))
                maya.cmds.setAttr('{}.color2R'.format(blend), 1)
                attr = attr_utils.NumericAttribute('stretchyBulge')
                attr.set_min_value(0)
                attr.set_max_value(10)
                attr.set_keyable(True)
                attr.create(node_for_attribute)
                attr_utils.connect_multiply('{}.stretchyBulge'.format(node_for_attribute), '{}.blender'.format(blend), 0.1)
            else:
                blend_attr = '{}.outputX'.format(multiply_offset)
            if scale_axis == 'X':
                maya.cmds.connectAttr(blend_attr, '%s.scaleY' % jnt)
                maya.cmds.connectAttr(blend_attr, '%s.scaleZ' % jnt)
            if scale_axis == 'Y':
                maya.cmds.connectAttr(blend_attr, '%s.scaleX' % jnt)
                maya.cmds.connectAttr(blend_attr, '%s.scaleZ' % jnt)
            if scale_axis == 'Z':
                maya.cmds.connectAttr(blend_attr, '%s.scaleX' % jnt)
                maya.cmds.connectAttr(blend_attr, '%s.scaleY' % jnt)
        percent += segment


def create_simple_spline_ik_stretch(curve, joints, stretch_axis='Y'):
    """
    Stretchs joints on curve.
    Joints must be attached to a SplienIk.
    :param curve: str, name of the curve that joints are attached to via SplineIk
    :param joints: list(str), listo f joints attached to SplineIk
    :param stretch_axis: str, stretch axis
    :return:
    """
    arclen_node = maya.cmds.arclen(curve, ch=True, n=(tp.Dcc.find_unique_name('curveInfo_{}'.format(curve))))
    arclen_node = maya.cmds.rename(arclen_node, tp.Dcc.find_unique_name('curveInfo_{}'.format(curve)))
    multiply_scale_offset = maya.cmds.createNode('multiplyDivide',
      n=(tp.Dcc.find_unique_name('multiplyDivide_offset_{}'.format(arclen_node))))
    maya.cmds.setAttr('{}.operation'.format(multiply_scale_offset), 2)
    multiply = maya.cmds.createNode('multiplyDivide',
      n=(tp.Dcc.find_unique_name('multiplyDivide_{}'.format(arclen_node))))
    maya.cmds.connectAttr('{}.arcLength'.format(arclen_node), '{}.input1X'.format(multiply_scale_offset))
    maya.cmds.connectAttr('{}.outputX'.format(multiply_scale_offset), '{}.input1X'.format(multiply))
    maya.cmds.setAttr('{}.input2X'.format(multiply), maya.cmds.getAttr('{}.arcLength'.format(arclen_node)))
    maya.cmds.setAttr('{}.operation'.format(multiply), 2)
    joint_count = len(joints)
    segment = 1.0 / joint_count
    percent = 0
    for jnt in joints:
        attr = '{}.outputX'.format(multiply)
        maya.cmds.connectAttr(attr, '{}.scale{}'.format(jnt, stretch_axis))
        percent += segment