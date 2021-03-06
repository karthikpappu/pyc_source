# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mafju/current/icm/iis_cr/vipe/vipe/oozie/reader/handlers.py
# Compiled at: 2016-02-15 13:44:30
# Size of source mod 2**32: 5624 bytes
__author__ = 'Mateusz Kobos mkobos@icm.edu.pl'
from vipe.oozie.reader.utils import properties_to_dict, get_text, findall_to_text, find_to_text
from vipe.oozie.graph import DecisionCase, Decision, End, Kill, Fork, Join, Start, OtherAction, SubworkflowAction, JavaAction, StreamingMapReduceAction, JavaMapReduceAction, PigAction, HiveAction, FSAction, DistCPAction

def handle_action(elem):
    """
    Returns:
        a (name, Action) pair where name is a string.
    """
    name = elem.get('name')
    type_ = __get_action_type(elem)
    ok_node = elem.find('ok').get('to')
    error_node = elem.find('error').get('to')
    action_elem = elem.find(type_)
    configuration = __get_configuration(action_elem)
    if type_ == 'sub-workflow':
        app_path = action_elem.find('app-path').text
        propagate_configuration = action_elem.find('propagate-configuration') is not None
        return (
         name,
         SubworkflowAction(ok_node, error_node, configuration, app_path, propagate_configuration))
    if type_ == 'java':
        main_class = find_to_text(action_elem, 'main-class')
        args = findall_to_text(action_elem, 'arg')
        captures_output = action_elem.find('capture-output') is not None
        return (
         name,
         JavaAction(ok_node, error_node, configuration, main_class, args, captures_output))
    if type_ == 'map-reduce':
        streaming_elem = action_elem.find('streaming')
        pipes_elem = action_elem.find('pipes')
        if streaming_elem is not None:
            mapper = find_to_text(streaming_elem, 'mapper')
            reducer = find_to_text(streaming_elem, 'reducer')
            return (
             name,
             StreamingMapReduceAction(ok_node, error_node, configuration, mapper, reducer))
        else:
            if pipes_elem is not None:
                return (
                 name,
                 OtherAction(ok_node, error_node, configuration, action_elem.tag))
            return (name,
             JavaMapReduceAction(ok_node, error_node, configuration))
    else:
        if type_ == 'pig':
            script = find_to_text(action_elem, 'script')
            params = findall_to_text(action_elem, 'param')
            args = findall_to_text(action_elem, 'argument')
            return (
             name,
             PigAction(ok_node, error_node, configuration, script, params, args))
        else:
            if type_ == 'hive':
                script = find_to_text(action_elem, 'script')
                params = findall_to_text(action_elem, 'param')
                return (
                 name,
                 HiveAction(ok_node, error_node, configuration, script, params))
            if type_ == 'fs':
                return (name, FSAction(ok_node, error_node))
            if type_ == 'distcp':
                args = [e.text for e in action_elem.findall('arg')]
                src_dst_args = [a for a in args if not a.startswith('-')]
                assert len(src_dst_args) == 2
                return (
                 name,
                 DistCPAction(ok_node, error_node, src_dst_args[0], src_dst_args[1]))
            return (name,
             OtherAction(ok_node, error_node, configuration, action_elem.tag))


def __get_configuration(action_elem):
    configuration = {}
    configuration_elem = action_elem.find('configuration')
    if configuration_elem is not None:
        configuration = properties_to_dict(configuration_elem)
    return configuration


def __get_action_type(elem):
    for child in elem:
        if child.tag not in ('ok', 'error'):
            return child.tag

    raise Exception('Action definition not found in elem={}'.format(elem))


def handle_fork(elem):
    name = elem.get('name')
    ends = []
    for found in elem.findall('path'):
        ends.append(found.get('start'))

    return (
     name, Fork(ends))


def handle_join(elem):
    name = elem.get('name')
    to = elem.get('to')
    return (name, Join(to))


def handle_decision(elem):
    name = elem.get('name')
    cases = []
    default_node = None
    for switch in elem.findall('switch'):
        for case in switch:
            to = case.get('to')
            tag = case.tag
            if tag == 'case':
                text = get_text(case)
                cases.append(DecisionCase(text, to))
            elif tag == 'default':
                assert default_node is None
                default_node = case.get('to')
            else:
                raise Exception('Unknown case tag "{}"'.format(tag))

    return (
     name, Decision(cases, default_node))


def handle_start(elem):
    return (
     'start', Start(elem.get('to')))


def handle_end(elem):
    name = elem.get('name')
    return (name, End())


def handle_kill(elem):
    name = elem.get('name')
    return (name, Kill())