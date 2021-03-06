# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dbbase/serializers.py
# Compiled at: 2020-05-03 12:32:54
# Size of source mod 2**32: 4978 bytes
"""
This module implements serializations.
"""
from datetime import date, datetime
from decimal import Decimal
import uuid
SA_INDICATOR = '_sa_instance_state'
DATE_FMT = '%F'
TIME_FMT = '%Y-%m-%d %H:%M:%S'
STOP_VALUE = '%%done%%'
SERIAL_STOPLIST = [
 '_class',
 '_decl_class_registry',
 '_sa_class_manager',
 '_sa_instance_state',
 'db',
 'delete',
 'deserialize',
 'get_serial_field_list',
 'metadata',
 'query',
 'save',
 'serialize',
 'to_dict',
 'validate_record',
 'SERIAL_STOPLIST',
 'SERIAL_LIST',
 'RELATION_SERIAL_LISTS']

def _eval_value(value, to_camel_case, level_limits, source_class, relation_serial_lists):
    """ _eval_value

    This function converts some of the standard values as needed based
    upon type. The more complex values are farmed out, such as for lists
    and models.

    parameters:
        value
            what is to be evaluated and perhaps converted

        to_camel_case
            Boolean for converting keys to camel case

        level_limits
            set of classes that have been visited already
            it is to prevent infinite recursion situations
        source_class

    returns
        values that have been converted as needed
    """
    if isinstance(value, datetime):
        result = value.strftime(TIME_FMT)
    else:
        if isinstance(value, date):
            result = value.strftime(DATE_FMT)
        else:
            if isinstance(value, Decimal):
                result = str(value)
            else:
                if isinstance(value, uuid.UUID):
                    result = str(value).replace('-', '')
                else:
                    if isinstance(value, list):
                        if len(value) > 0:
                            result, level_limits = _eval_value_list(value, to_camel_case, level_limits, source_class, relation_serial_lists)
                        else:
                            result = []
                    elif hasattr(value, 'to_dict'):
                        result, level_limits = _eval_value_model(value, to_camel_case, level_limits, source_class, relation_serial_lists)
                    else:
                        result = value
    return result


def _eval_value_model(value, to_camel_case, level_limits, source_class, relation_serial_lists):
    """_eval_value_model

    if any class within level_limits i self-referential it gets
    passed on.
    """
    result = STOP_VALUE
    class_name = value._class()
    if class_name in level_limits:
        if not value._has_self_ref:
            return result
    serial_list = value.SERIAL_LIST
    if class_name in relation_serial_lists:
        serial_list = relation_serial_lists[class_name]
    if source_class is not None:
        level_limits.add(source_class)
    result = value.to_dict(to_camel_case,
      level_limits=level_limits,
      serial_list=serial_list,
      relation_serial_lists=relation_serial_lists)
    level_limits.add(class_name)
    return (
     result, level_limits)


def _eval_value_list(value, to_camel_case, level_limits, source_class, relation_serial_lists):
    """_eval_value_list

    This function handles values that are lists. While a list that is not
    a model is pretty straight-forward, a list of models is a little
    trickier.

    If a model is self-referential, such as a node, the model should be
    passed on to be evaluated. However, if it is not, such as
        user > addresses > user,
    then if the model has not already been evaluated, it should be.
    But, it should be for each line in the list, so you can't mark it as
    done until all the lines have been processed. The approach taken here is
    to make a temporary level_limits set, pass it in, but start it fresh
    for the next line. Only at the end should level_limits be updated.

    """
    tmp_list = []
    tmp_limits = None
    for item in value:
        tmp_limits = level_limits.copy()
        if hasattr(item, 'to_dict'):
            status = True
            result = STOP_VALUE
            if item._class() in level_limits:
                if not item._has_self_ref():
                    status = False
            if status:
                result, tmp_limits = _eval_value_model(item, to_camel_case, tmp_limits, source_class, relation_serial_lists)
        else:
            result = _eval_value(item, to_camel_case, tmp_limits, source_class, relation_serial_lists)
        tmp_list.append(result)

    if all(list(map(lambda i: i == STOP_VALUE, tmp_list))):
        tmp_list = STOP_VALUE
    if tmp_limits is not None:
        level_limits = tmp_limits.copy()
    return (tmp_list, level_limits)