# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpDcc/dccs/maya/core/space.py
# Compiled at: 2020-05-13 19:28:33
# Size of source mod 2**32: 8489 bytes
"""
Module that contains functions and classes related with spaces
"""
from __future__ import print_function, division, absolute_import
import logging
from tpDcc.libs.python import python
import tpDcc.dccs.maya as maya
from tpDcc.dccs.maya.core import name as name_utils, attribute as attr_utils, transform as xform_utils
from tpDcc.dccs.maya.core import constraint as cns_utils
LOGGER = logging.getLogger()

def create_follow_group(source_transform, target_transform, prefix='follow', follow_scale=False, use_duplicate=False):
    """
    Creates a group above a target transform that is constrained to the source transform
    :param source_transform: str, name of the transform to follow
    :param target_transform: str, name of the transform make follow
    :param prefix: str, prefix to add to the follow group
    :param follow_scale: bool, Whether to ad a scale constraint or not
    :param use_duplicate: bool, Whether to use a duplicate or not
    :return: str, name of the follow group
    """
    parent = maya.cmds.listRelatives(target_transform, p=True, f=True)
    target_name = python.force_list(target_transform)
    name = '{}_{}'.format(prefix, target_name[0])
    if use_duplicate:
        follow_group = maya.cmds.duplicate(target_transform, n=(name_utils.find_unique_name(name)), po=True)[0]
        attr_utils.remove_user_defined_attributes(follow_group)
        parent = None
    else:
        follow_group = maya.cmds.group(empty=True, n=(name_utils.find_unique_name(name)))
    match = xform_utils.MatchTransform(source_transform, follow_group)
    match.translation_rotation()
    if parent:
        maya.cmds.parent(follow_group, parent)
    if follow_scale:
        attr_utils.connect_scale(source_transform, follow_group)
    maya.cmds.parentConstraint(source_transform, follow_group, mo=True)
    return follow_group


def create_local_follow_group(source_transform, target_transform, prefix='followLocal', orient_only=False, connect_scale=False):
    """
    Creates a group above a target transform that is local constrained to the source transform
    This help when setting up controls that need to be parented but only affect what they constrain when the actual
    control is moved
    :param source_transform: str, transform to follow
    :param target_transform: str, transform to make follow
    :param prefix: str, prefix to add to the follow group
    :param orient_only: bool, Whether the local constraint should just be an orient constraint
    :param connect_scale: bool, Whether local constraint should constraint also scale or not
    """
    parent = maya.cmds.listRelatives(target_transform, p=True)
    name = '{}_{}'.format(prefix, target_transform)
    follow_group = maya.cmds.group(empty=True, n=(name_utils.find_unique_name(name)))
    match = xform_utils.MatchTransform(source_transform, follow_group)
    match.translation_rotation()
    xform_grp = xform_utils.create_buffer_group(follow_group)
    if not orient_only:
        attr_utils.connect_translate(source_transform, follow_group)
    if orient_only or not orient_only:
        attr_utils.connect_rotate(source_transform, follow_group)
    if connect_scale:
        attr_utils.connect_scale(source_transform, follow_group)
    maya.cmds.parent(target_transform, follow_group)
    if parent:
        maya.cmds.parent(xform_grp, parent)
    return follow_group


def create_multi_follow_direct(source_list, target_transform, node, constraint_type='parentConstraint', attribute_name='follow', value=None):
    """
    Creates a group above the target that is constrained to multiple transforms. A switch attribute switches their
    state on/off. Constraints will be "directly" added on the target transform
    :param source_list: list(str), list of transforms that the target should be constrained by
    :param target_transform: str, name of a transform node that should follow the transforms in source_list
    :param node: str, name of the node to add the swtich attribute to
    :param constraint_type: str, Maya constraint type ('parentConstraint', 'pointConstraint' or 'orientConstraint')
    :param attribute_name: str, name of the swtich attribute t oadd to the the node
    :param value: float, value to give the switch attribute on the node
    :return: str, name of the new group
    """
    locators = list()
    if attribute_name == 'follow':
        var = attr_utils.EnumAttribute('FOLLOW')
        var.create(node)
    else:
        for source in source_list:
            locator = maya.cmds.spaceLocator(n=(name_utils.find_unique_name('follower_1_{}'.format(source), False)))[0]
            maya.cmds.hide(locator)
            match = xform_utils.MatchTransform(target_transform, locator)
            match.translation_rotation()
            maya.cmds.parent(locator, source)
            locators.append(locator)

        if constraint_type == 'parentConstraint':
            constraint = maya.cmds.parentConstraint(locators, target_transform, mo=True)[0]
            maya.cmds.setAttr('{}.interpType'.format(constraint), 2)
        else:
            if constraint_type == 'pointConstraint':
                constraint = maya.cmds.pointConstraint(locators, target_transform, mo=True)[0]
            else:
                if constraint_type == 'orientConstraint':
                    constraint = maya.cmds.orientConstraint(locators, target_transform, mo=True)[0]
                    maya.cmds.setAttr('{}.interpType'.format(constraint), 2)
                else:
                    raise RuntimeError('Constraint Type: "{}" is not supported!'.format(constraint_type))
    constraint_editor = cns_utils.Constraint()
    constraint_editor.create_switch(node, attribute_name, constraint)
    if value is None:
        value = len(source_list) - 1
    maya.cmds.setAttr('{}.{}'.format(node, attribute_name), value)
    return target_transform


def create_multi_follow(source_list, target_transform, node=None, constraint_type='parentConstraint', attribute_name='follow', value=None, create_title=True):
    """
    Creates a group above the target that is constrained to multiple transforms. A switch attribute switches their
    state on/off. Constraints will be "directly" added on the target transform
    :param source_list: list(str), list of transforms that the target should be constrained by
    :param target_transform: str, name of a transform node that should follow the transforms in source_list
    :param node: str, name of the node to add the swtich attribute to
    :param constraint_type: str, Maya constraint type ('parentConstraint', 'pointConstraint' or 'orientConstraint')
    :param attribute_name: str, name of the swtich attribute t oadd to the the node
    :param value: float, value to give the switch attribute on the node
    :param create_title: bool
    :return: str, name of the new group
    """
    if len(source_list) < 2:
        LOGGER.warning('Cannot create mlti follow with less than 2 source transforms!')
        return False
    else:
        locators = list()
        if node is None:
            node = target_transform
        follow_group = xform_utils.create_buffer_group(target_transform, 'follow')
        title_name = attribute_name.upper()
        for source in source_list:
            locator = maya.cmds.spaceLocator(n=(name_utils.find_unique_name('follower_1_{}'.format(source), False)))[0]
            maya.cmds.hide(locator)
            match = xform_utils.MatchTransform(target_transform, locator)
            match.translation_rotation()
            maya.cmds.parent(locator, source)
            locators.append(locator)

        if constraint_type == 'parentConstraint':
            constraint = maya.cmds.parentConstraint(locators, follow_group, mo=True)[0]
            maya.cmds.setAttr('{}.interpType'.format(constraint), 2)
        else:
            if constraint_type == 'pointConstraint':
                constraint = maya.cmds.pointConstraint(locators, follow_group, mo=True)[0]
            else:
                if constraint_type == 'orientConstraint':
                    constraint = maya.cmds.orientConstraint(locators, follow_group, mo=True)[0]
                    maya.cmds.setAttr('{}.interpType'.format(constraint), 2)
                else:
                    raise RuntimeError('Constraint Type: "{}" is not supported!'.format(constraint_type))
        constraint_editor = cns_utils.Constraint()
        if create_title:
            constraint_editor.create_title(node, constraint, title_name)
        constraint_editor.create_switch(node, attribute_name, constraint)
        if value is None:
            value = len(source_list) - 1
        maya.cmds.setAttr('{}.{}'.format(node, attribute_name), value)
        return follow_group