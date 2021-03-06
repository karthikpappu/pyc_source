# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vortex/repos/FENIX-MAPS/geobricks/geobricks_metadata_manager/geobricks_metadata_manager/rest/metadata_manager_rest.py
# Compiled at: 2015-01-08 04:45:00
import json, os
from flask import Blueprint
from flask import Response
from flask.ext.cors import cross_origin
from geobricks_metadata_manager.utils.log import logger
from geobricks_metadata_manager.config.config import config
from geobricks_metadata_manager.core.metadata_manager_d3s_core import MetadataManager
log = logger(__file__)
app = Blueprint('metadata_manager', 'metadata_manager')

@app.route('/discovery/')
@app.route('/discovery')
@cross_origin(origins='*')
def discovery():
    """
    Discovery service available for all Geobricks libraries that describes the plug-in.
    @return: Dictionary containing information about the service.
    """
    out = {'name': 'Metadata Manager', 
       'description': 'Metadata manager services.', 
       'type': 'SERVICE'}
    return Response(json.dumps(out), content_type='application/json; charset=utf-8')


@app.route('/query/uid/<uid>/', methods=['GET'])
@app.route('/query/uid/<uid>', methods=['GET'])
@cross_origin(origins='*')
def query_by_uid(uid):
    """
    Find a D3S resource by uid.
    :param name: uid of the resource
    :return: json containing the D3S response
    """
    metadata_manager = MetadataManager(config)
    result = metadata_manager.get_by_uid(uid)
    return Response(json.dumps(result), content_type='application/json; charset=utf-8')