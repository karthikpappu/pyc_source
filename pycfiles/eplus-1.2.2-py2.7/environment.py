# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/eplus/environment.py
# Compiled at: 2019-09-05 08:50:09
import os, sys, re, yaml
from .utils import find_sdk, find_gcloud_lib
APP_YAML_FILE = os.path.isfile('app-remote.yaml') and 'app-remote.yaml' or 'app.yaml'
APP_YAML_LOCAL_FILE = os.path.isfile('app-local.yaml') and 'app-local.yaml' or 'app.yaml'

def init():
    if 'google' in sys.modules:
        del sys.modules['google']
    sdk_root = find_sdk()
    if sdk_root not in sys.path:
        sys.path.append(sdk_root)
    from dev_appserver import _PATHS
    sys.path[1:1] = _PATHS.v2_extra_paths
    sys.path[1:1] = _PATHS._script_to_paths.get('dev_appserver.py')
    sys.path.append(os.path.abspath('.'))
    try:
        import appengine_config
    except ImportError:
        pass


def init_lib():
    lib_root = find_gcloud_lib()
    if lib_root not in sys.path:
        sys.path.append(lib_root)


def setup_remote():
    args = sys.argv[1:]
    if len(args) < 1 or not args[0].endswith('.yaml'):
        args.insert(0, APP_YAML_FILE)
    from google.appengine.tools.devappserver2.devappserver2 import PARSER
    options = PARSER.parse_args(args)
    yaml_file = options.config_paths[0]
    with open(yaml_file, 'r') as (fh):
        yaml_data = yaml.safe_load(fh)
        env_extra = yaml_data.get('env_variables', {})
        os.environ.update(env_extra)
    from google.appengine.tools.devappserver2.devappserver2 import application_configuration
    configuration = application_configuration.ApplicationConfiguration(options.config_paths, options.app_id)
    mc = configuration.modules[0]
    host = ('-dot-').join((mc.major_version, mc.module_name, mc.application_external_name)) + '.appspot.com'
    if 'HTTP_HOST' not in os.environ:
        os.environ['HTTP_HOST'] = host
        os.environ['APPLICATION_ID'] = configuration.app_id
    os.environ['SERVER_SOFTWARE'] = 'Development (remote_api)/1.0'
    from google.appengine.ext.remote_api import remote_api_stub
    remote_api_stub.ConfigureRemoteApiForOAuth(host, '/_ah/remote_api')


def setup_local():
    from google.appengine.tools.devappserver2.devappserver2 import PARSER
    options = PARSER.parse_args([APP_YAML_LOCAL_FILE])
    from google.appengine.tools.devappserver2.devappserver2 import application_configuration
    configuration = application_configuration.ApplicationConfiguration(options.config_paths, options.app_id)
    os.environ['HTTP_HOST'] = 'localhost'
    os.environ['APPLICATION_ID'] = configuration.app_id
    os.environ['AUTH_DOMAIN'] = 'localhost'
    os.environ['SERVER_NAME'] = 'localhost'
    os.environ['SERVER_PORT'] = '8080'
    try:
        from google.appengine.tools.devappserver2.api_server import get_storage_path
    except ImportError:
        from google.appengine.tools.devappserver2.devappserver2 import _get_storage_path as get_storage_path

    storage_path = get_storage_path(options.storage_path, configuration.app_id)
    setup_stubs(storage_path, options, configuration)


def setup_stubs(storage_path, options, configuration):
    datastore_path = options.datastore_path or os.path.join(storage_path, 'datastore.db')
    search_index_path = options.search_indexes_path or os.path.join(storage_path, 'search_indexes')
    blobstore_path = options.blobstore_path or os.path.join(storage_path, 'blobs')
    from google.appengine.api import apiproxy_stub_map
    apiproxy_stub_map.apiproxy = apiproxy_stub_map.APIProxyStubMap()
    from google.appengine.datastore import datastore_sqlite_stub
    apiproxy_stub_map.apiproxy.RegisterStub('datastore_v3', datastore_sqlite_stub.DatastoreSqliteStub(configuration.app_id, datastore_path))
    from google.appengine.api.search import simple_search_stub
    apiproxy_stub_map.apiproxy.RegisterStub('search', simple_search_stub.SearchServiceStub(index_file=search_index_path))
    from google.appengine.api.blobstore import file_blob_storage
    blob_storage = file_blob_storage.FileBlobStorage(blobstore_path, configuration.app_id)
    from google.appengine.api.blobstore import blobstore_stub
    apiproxy_stub_map.apiproxy.RegisterStub('blobstore', blobstore_stub.BlobstoreServiceStub(blob_storage))
    from google.appengine.api.app_identity import app_identity_stub
    apiproxy_stub_map.apiproxy.RegisterStub('app_identity_service', app_identity_stub.AppIdentityServiceStub())
    from google.appengine.api.capabilities import capability_stub
    apiproxy_stub_map.apiproxy.RegisterStub('capability_service', capability_stub.CapabilityServiceStub())
    from google.appengine.api.memcache import memcache_stub
    apiproxy_stub_map.apiproxy.RegisterStub('memcache', memcache_stub.MemcacheServiceStub())
    from google.appengine.api.taskqueue import taskqueue_stub
    apiproxy_stub_map.apiproxy.RegisterStub('taskqueue', taskqueue_stub.TaskQueueServiceStub())
    from google.appengine.api import urlfetch_stub
    apiproxy_stub_map.apiproxy.RegisterStub('urlfetch', urlfetch_stub.URLFetchServiceStub())


def tear_down_local():
    from google.appengine.tools.devappserver2.api_server import cleanup_stubs
    cleanup_stubs()