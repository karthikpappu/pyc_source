# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/api/v1/rgw.py
# Compiled at: 2016-06-13 14:11:03
"""The rgws api."""
import platform
from vsm.api.openstack import wsgi
from vsm.api.views import mdses as mds_views
from vsm import conductor
from vsm import exception
from vsm import flags
from vsm.openstack.common import log as logging
from vsm import scheduler
from vsm import utils
LOG = logging.getLogger(__name__)
FLAGS = flags.FLAGS

class RgwController(wsgi.Controller):
    """The rgw API controller for the VSM API."""
    _view_builder_class = mds_views.ViewBuilder

    def __init__(self, ext_mgr):
        self.conductor_api = conductor.API()
        self.scheduler_api = scheduler.API()
        self.ext_mgr = ext_mgr
        super(RgwController, self).__init__()

    def create(self, req, body):
        """
        Create a rgw.
        :param req:
        :param body:
        {
            "rgw": {
                "rgw_info": {
                    "server_name": "rgw-node1",
                    "rgw_instance_name": "radosgw.gateway",
                    "is_ssl": False
                },
                "user_info": {
                    "uid": "johndoe",
                    "display_name": "John Doe",
                    "email": "john@example.comjohn@example.com",
                    "sub_user": "johndoe:swift",
                    "access": "full",
                    "key_type": "swift"
                }
            }
        }
        :return:
        """
        context = req.environ['vsm.context']

        def _get_os():
            distro, release, codename = platform.dist()
            return distro

        distro = _get_os()
        if distro.lower() == 'centos':
            try:
                utils.execute('ls', '/usr/bin/radosgw', run_as_root=True)
            except:
                LOG.error('Not installed ceph-radosgw')
                raise exception.VsmException()

        elif distro.lower() == 'ubuntu':
            try:
                utils.execute('ls', '/usr/bin/radosgw', run_as_root=True)
            except:
                LOG.error('Not installed radosgw')
                raise exception.VsmException()

        rgw = body['rgw']
        rgw_info = rgw['rgw_info']
        user_info = rgw['user_info']
        server_name = rgw_info.get('server_name', '')
        if not server_name:
            LOG.error('No server to create rgw.')
            raise exception.VsmException()
        rgw_instance_name = rgw_info.get('rgw_instance_name', '')
        if not rgw_instance_name:
            rgw_instance_name = 'gateway'
            LOG.warn("rgw instance name uses default name 'rgw'")
        is_ssl = rgw_info.get('is_ssl', '')
        if is_ssl == '':
            is_ssl = False
            LOG.warn('do not use ssl')
        uid = user_info.get('uid') if user_info.get('uid', '') else 'johndoe'
        display_name = user_info.get('display_name') if user_info.get('display_name', '') else 'John Doe'
        email = user_info.get('email') if user_info.get('email', '') else 'john@example.comjohn@example.com'
        sub_user = user_info.get('sub_user') if user_info.get('sub_user', '') else 'johndoe:swift'
        access = user_info.get('access') if user_info.get('access', '') else 'full'
        key_type = user_info.get('key_type') if user_info.get('key_type', '') else 'swift'
        self.scheduler_api.rgw_create(context, server_name, rgw_instance_name, is_ssl, uid, display_name, email, sub_user, access, key_type)


def create_resource(ext_mgr):
    return wsgi.Resource(RgwController(ext_mgr))