# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xbus/monitor/views/api/emission_profile.py
# Compiled at: 2016-06-27 04:20:00
# Size of source mod 2**32: 2492 bytes
from pyramid.httpexceptions import HTTPBadRequest
from pyramid.response import Response
from xbus.monitor.auth import get_logged_user_id
from xbus.monitor.models.monitor import DBSession
from xbus.monitor.models.monitor import EmissionProfile
from .util import get_list
from .util import get_record
from . import view_decorators
_MODEL = 'emission_profile'

def _update_record(request, record):
    """Update the record using JSON data."""
    try:
        vals = request.json_body
        record.input_descriptor_id = vals['input_descriptor_id']
        record.input_type = vals.get('input_type', 'descriptor')
        record.name = vals['name']
        record.encoding = vals['encoding']
    except (KeyError, ValueError):
        raise HTTPBadRequest(json_body={'error': 'Invalid data'})


@view_decorators.list(_MODEL)
def emission_profile_list(request):

    def wrapper(ev):
        """a small wrapper to add the input_descriptor_name key to the resulting
        records of the list
        """
        ret = ev.as_dict()
        if ev.input_descriptor:
            ret['input_descriptor_name'] = ev.input_descriptor.name
        else:
            ret['input_descriptor_name'] = ''
        return ret

    ret = get_list(EmissionProfile, request.GET, record_wrapper=wrapper)
    return [ret[0],
     [item for item in ret[1] if item['owner_id'] == get_logged_user_id(request)]]


@view_decorators.create(_MODEL)
def emission_profile_create(request):
    record = EmissionProfile()
    record.owner_id = get_logged_user_id(request)
    _update_record(request, record)
    DBSession.add(record)
    DBSession.flush()
    DBSession.refresh(record)
    return record.as_dict()


@view_decorators.read(_MODEL)
def emission_profile_read(request):
    record = get_record(request, _MODEL)
    return record.as_dict()


@view_decorators.update(_MODEL)
def emission_profile_update(request):
    record = get_record(request, _MODEL)
    _update_record(request, record)
    return record.as_dict()


@view_decorators.delete(_MODEL)
def emission_profile_delete(request):
    record = get_record(request, _MODEL)
    DBSession.delete(record)
    return Response(status_int=204, json_body={})