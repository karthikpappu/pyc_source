# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: F:\GitCode\trangevi-azurecli\azure\cli\command_modules\ml\service\_realtime_mms.py
# Compiled at: 2017-10-10 11:52:57
import json, os, requests, sys
from azure.cli.core.util import CLIError
from pkg_resources import resource_string
from ._realtimeutilities import get_sample_data
from .._constants import APP_INSIGHTS_URL
from .._constants import MLC_API_VERSION
from .._constants import DEFAULT_INPUT_DATA
from .._constants import MLC_RESOURCE_ID_FMT
from .._constants import MMS_API_VERSION
from .._constants import MMS_OPERATION_URL_ENDPOINT
from .._constants import MMS_SERVICE_CREATE_OPERATION_POLLING_MAX_TRIES
from .._constants import MMS_SERVICE_LIST_KEYS_URL_ENDPOINT
from .._constants import MMS_SERVICE_REGEN_KEYS_URL_ENDPOINT
from .._constants import MMS_SERVICE_URL_ENDPOINT
from .._constants import MMS_SYNC_TIMEOUT_SECONDS
from .._constants import SUCCESS_RETURN_CODE
from .._constants import SWAGGER_URI_FORMAT
from .._get_logs import get_logs_from_kubernetes
from .._k8s_util import check_for_kubectl
from .._util import conditional_update_or_remove
from .._util import get_auth_header
from .._util import get_current_model_management_url_base
from .._util import get_json
from .._util import get_paginated_results
from .._util import poll_mms_async_operation
from .._util import str_to_bool

def mms_service_create(image_id, service_name, app_insights_logging_enabled, model_data_collection_enabled, num_replicas, autoscale_enabled, autoscale_min_replicas, autoscale_max_replicas, autoscale_target_utilization, autoscale_refresh_period_seconds, cpu, memory, replica_max_concurrent_requests, verb, context):
    auth_header = get_auth_header()
    headers = {'Content-Type': 'application/json', 'Authorization': auth_header}
    params = {'api-version': MMS_API_VERSION}
    service_url = get_current_model_management_url_base() + MMS_SERVICE_URL_ENDPOINT
    json_payload = json.loads(resource_string(__name__, 'data/mmsservicepayloadtemplate.json').decode('ascii'))
    json_payload['imageId'] = image_id
    json_payload['name'] = service_name
    if num_replicas:
        json_payload['numReplicas'] = num_replicas
    else:
        del json_payload['numReplicas']
    json_payload['computeResource']['id'] = MLC_RESOURCE_ID_FMT.format(context.current_compute_subscription_id, context.current_compute_resource_group, context.current_compute_name)
    if model_data_collection_enabled is None:
        del json_payload['dataCollection']
    else:
        json_payload['dataCollection']['storageEnabled'] = model_data_collection_enabled
        json_payload['dataCollection']['eventHubEnabled'] = False
    if app_insights_logging_enabled is None:
        del json_payload['appInsightsEnabled']
    else:
        json_payload['appInsightsEnabled'] = app_insights_logging_enabled
    if autoscale_enabled is None:
        del json_payload['autoScaler']['autoscaleEnabled']
    else:
        if autoscale_enabled:
            json_payload['autoScaler']['autoscaleEnabled'] = True
            del json_payload['numReplicas']
        conditional_update_or_remove(json_payload, ('autoScaler', 'minReplicas'), autoscale_min_replicas)
        conditional_update_or_remove(json_payload, ('autoScaler', 'maxReplicas'), autoscale_max_replicas)
        conditional_update_or_remove(json_payload, ('autoScaler', 'targetUtilization'), autoscale_target_utilization)
        conditional_update_or_remove(json_payload, ('autoScaler', 'refreshPeriodInSeconds'), autoscale_refresh_period_seconds)
        conditional_update_or_remove(json_payload, ('containerResourceReservation',
                                                    'cpu'), cpu)
        conditional_update_or_remove(json_payload, ('containerResourceReservation',
                                                    'memory'), memory)
        conditional_update_or_remove(json_payload, ('maxConcurrentRequestsPerContainer', ), replica_max_concurrent_requests)
        if verb:
            print ('Sending the following payload to {}\n{}').format(service_url, json_payload)
        try:
            resp = context.http_call('post', service_url, params=params, headers=headers, json=json_payload, timeout=MMS_SYNC_TIMEOUT_SECONDS)
        except requests.ConnectionError:
            raise CLIError(('Error connecting to {}.').format(service_url))
        except requests.Timeout:
            raise CLIError(('Error, request to {} timed out.').format(service_url))

        if resp.status_code != 202:
            raise CLIError(('Error occurred creating service.\nStatus Code: {}\nHeaders: {}\nContent: {}').format(resp.status_code, resp.headers, resp.content))
        try:
            operation_location = resp.headers['Operation-Location']
        except KeyError:
            raise CLIError('Invalid response header key: Operation-Location')

        create_operation_status_id = operation_location.split('/')[(-1)]
        if verb:
            print ('Operation Id: {}').format(create_operation_status_id)
        operation_url = get_current_model_management_url_base() + MMS_OPERATION_URL_ENDPOINT.format(create_operation_status_id)
        operation_headers = {'Authorization': auth_header}
        sys.stdout.write('Creating service')
        sys.stdout.flush()
        service_id = poll_mms_async_operation(operation_url, operation_headers, params, MMS_SERVICE_CREATE_OPERATION_POLLING_MAX_TRIES, context)
        service_url = service_url + ('/{}').format(service_id)
        input_data = None
        try:
            resp = context.http_call('get', service_url, params=params, headers=headers, timeout=MMS_SYNC_TIMEOUT_SECONDS)
            if resp.status_code == 200:
                service = get_json(resp.content, pascal=True)
                scoring_url = service['ScoringUri']
                swagger_url = SWAGGER_URI_FORMAT.format(('/').join(scoring_url.split('/')[:-1]))
                keys_url = service_url + '/keys'
                keys_resp = context.http_call('get', keys_url, params=params, headers=headers, timeout=MMS_SYNC_TIMEOUT_SECONDS)
                if keys_resp.status_code == 200:
                    service_keys = get_json(keys_resp.content, pascal=True)
                    scoring_headers = {'Authorization': ('Bearer {}').format(service_keys['PrimaryKey'])}
                    input_data = get_sample_data(swagger_url, headers=scoring_headers, verbose=verb)
                else:
                    print 'Error occurred while attempting to get service swagger information.'
            else:
                print 'Error occurred while attempting to get service swagger information.'
        except (requests.ConnectionError, requests.Timeout, KeyError):
            print 'Error occurred while attempting to get service swagger information.'

    if not input_data:
        input_data = DEFAULT_INPUT_DATA
    print 'Done'
    print ('Service ID: {}').format(service_id)
    if context.os_is_unix():
        print ('Usage: az ml service run realtime -i {} -d {}').format(service_id, input_data)
    else:
        print ('Usage for cmd: az ml service run realtime -i {} -d {}').format(service_id, input_data)
        print ('Usage for powershell: az ml service run realtime -i {} --% -d {}').format(service_id, input_data)
    print ("Additional usage information: 'az ml service usage realtime -i {}'").format(service_id)
    if app_insights_logging_enabled:
        try:
            app_insights_id = context.current_env['app_insights']['resourceId'].split('/')[(-1)]
            print ('App insights logs can be found here: {}').format(APP_INSIGHTS_URL.format(context.current_compute_subscription_id, context.current_compute_resource_group, app_insights_id))
        except:
            pass

    return (
     SUCCESS_RETURN_CODE, service_id)


def mms_service_run(service_id, input_data, verb, context):
    scoring_headers = {'Content-Type': 'application/json'}
    auth_header = get_auth_header()
    mms_headers = {'Authorization': auth_header}
    params = {'api-version': MMS_API_VERSION}
    service_url = get_current_model_management_url_base() + MMS_SERVICE_URL_ENDPOINT + ('/{}').format(service_id)
    try:
        resp = context.http_call('get', service_url, params=params, headers=mms_headers, timeout=MMS_SYNC_TIMEOUT_SECONDS)
    except requests.ConnectionError:
        raise CLIError(('Error connecting to {}.').format(service_url))
    except requests.Timeout:
        raise CLIError(('Error, request to {} timed out.').format(service_url))

    if resp.status_code == 200:
        endpoint_obj = get_json(resp.content, pascal=True)
        try:
            scoring_endpoint = endpoint_obj['ScoringUri']
        except KeyError:
            raise CLIError(("Error occured attempting to retrieve scoring endpoint for service.\n'ScoringUri' not present in service payload: {}").format(endpoint_obj))

        if verb:
            print ('Successfully got service to score against\nStatus Code: {}\nHeaders: {}\nContent: {}').format(resp.status_code, resp.headers, resp.content)
    else:
        raise CLIError(('Error occurred while attempting to retrieve service {} to score against.\nStatus Code: {}\nHeaders: {}\nContent: {}').format(service_id, resp.status_code, resp.headers, resp.content))
    keys_url = service_url + '/keys'
    try:
        resp = context.http_call('get', keys_url, params=params, headers=mms_headers, timeout=MMS_SYNC_TIMEOUT_SECONDS)
    except requests.ConnectionError:
        raise CLIError(('Error connecting to {}.').format(service_url))
    except requests.Timeout:
        raise CLIError(('Error, request to {} timed out.').format(service_url))

    if resp.status_code == 200:
        if verb:
            print ('Successfully got keys for service\nStatus Code: {}\nHeaders: {}\nContent: {}').format(resp.status_code, resp.headers, resp.content)
        service_keys = get_json(resp.content, pascal=True)
        scoring_headers['Authorization'] = ('Bearer {}').format(service_keys['PrimaryKey'])
    else:
        raise CLIError(('Error occurred while attempting to retrieve service keys.\nStatus Code: {}\nHeaders: {}\nContent: {}').format(resp.status_code, resp.headers, resp.content))
    if input_data == '':
        print 'No input data specified. Checking for sample data.'
        swagger_url = SWAGGER_URI_FORMAT.format(('/').join(scoring_endpoint.split('/')[:-1]))
        sample_data = get_sample_data(swagger_url, scoring_headers, verb)
        if sample_data:
            input_data = sample_data
            print 'Using sample data: ' + input_data
    else:
        if verb:
            print ('[Debug] Input data is {}').format(input_data)
            print ('[Debug] Input data type is {}').format(type(input_data))
        result = requests.post(scoring_endpoint, data=input_data, headers=scoring_headers, timeout=MMS_SYNC_TIMEOUT_SECONDS)
        if verb:
            print ('Got result from scoring request at {}.\nStatus Code: {}\nHeaders: {}\nContent: {}').format(scoring_endpoint, result.status_code, result.headers, result.content)
        if result.status_code == 200:
            result = result.json()
            print result
            return SUCCESS_RETURN_CODE
    content = result.content.decode()
    if content == 'ehostunreach':
        print 'Error scoring the service.'
        raise CLIError('Unable to reach the requested host.\nIf you just created this service, it may not be available yet. Please try again in a few minutes.')
    raise CLIError(('Error occurred while attempting to score service {}.\nStatus Code: {}\nHeaders: {}\nContent: {}').format(service_id, result.status_code, result.headers, result.content.decode('utf-8')))


def mms_service_update(service_id, image_id, num_replicas, model_data_collection_enabled, app_insights_enabled, autoscale_enabled, autoscale_min_replicas, autoscale_max_replicas, autoscale_target_utilization, autoscale_refresh_period_seconds, cpu, memory, replica_max_concurrent_requests, verb, context):
    auth_header = get_auth_header()
    headers = {'Content-Type': 'application/json', 'Authorization': auth_header}
    params = {'api-version': MMS_API_VERSION}
    service_url = get_current_model_management_url_base() + MMS_SERVICE_URL_ENDPOINT + ('/{}').format(service_id)
    json_payload = json.loads(resource_string(__name__, 'data/mmsservicepayloadtemplate.json').decode('ascii'))
    del json_payload['name']
    del json_payload['computeResource']
    if num_replicas:
        json_payload['numReplicas'] = num_replicas
    else:
        del json_payload['numReplicas']
    if model_data_collection_enabled:
        model_data_collection_bool = str_to_bool(model_data_collection_enabled)
        if model_data_collection_bool is None:
            raise CLIError(('Error, invalid value provided for model_data_collection_enabled: {}').format(model_data_collection_enabled))
        json_payload['dataCollection']['storageEnabled'] = model_data_collection_bool
    else:
        del json_payload['dataCollection']
    if app_insights_enabled:
        app_insights_bool = str_to_bool(app_insights_enabled)
        if app_insights_bool is None:
            raise CLIError(('Error, invalid value provided for app_insights_enabled: {}').format(app_insights_enabled))
        json_payload['appInsightsEnabled'] = app_insights_bool
    else:
        del json_payload['appInsightsEnabled']
    if not autoscale_enabled and not autoscale_min_replicas and not autoscale_max_replicas and not autoscale_target_utilization and not autoscale_refresh_period_seconds:
        del json_payload['autoScaler']
    else:
        if autoscale_enabled:
            autoscale_enabled_bool = str_to_bool(autoscale_enabled)
            if autoscale_enabled_bool is None:
                raise CLIError(('Error, invalid value provided for autoscale_enabled: {}').format(autoscale_enabled))
            json_payload['autoScaler']['autoscaleEnabled'] = autoscale_enabled_bool
        else:
            del json_payload['autoScaler']['autoscaleEnabled']
        conditional_update_or_remove(json_payload, ('autoScaler', 'minReplicas'), autoscale_min_replicas)
        conditional_update_or_remove(json_payload, ('autoScaler', 'maxReplicas'), autoscale_max_replicas)
        conditional_update_or_remove(json_payload, ('autoScaler', 'targetUtilization'), autoscale_target_utilization)
        conditional_update_or_remove(json_payload, ('autoScaler', 'refreshPeriodInSeconds'), autoscale_refresh_period_seconds)
    if not cpu and not memory:
        del json_payload['containerResourceReservation']
    else:
        conditional_update_or_remove(json_payload, ('containerResourceReservation',
                                                    'cpu'), cpu)
        conditional_update_or_remove(json_payload, ('containerResourceReservation',
                                                    'memory'), memory)
    conditional_update_or_remove(json_payload, ('maxConcurrentRequestsPerContainer', ), replica_max_concurrent_requests)
    if not image_id:
        result, service_payload = mms_service_show(None, service_id, verb, context)
        try:
            image_id = service_payload['Image']['Id']
        except KeyError:
            raise CLIError(('Unable to retrieve image id from service details: {}').format(service_payload))

    json_payload['imageId'] = image_id
    try:
        resp = context.http_call('put', service_url, params=params, headers=headers, json=json_payload, timeout=MMS_SYNC_TIMEOUT_SECONDS)
    except requests.ConnectionError:
        raise CLIError(('Error connecting to {}.').format(service_url))
    except requests.Timeout:
        raise CLIError(('Error, request to {} timed out.').format(service_url))

    if resp.status_code != 202:
        raise CLIError(('Error occurred updating service {}.\nStatus Code: {}\nHeaders: {}\nContent: {}').format(service_id, resp.status_code, resp.headers, resp.content))
    try:
        operation_location = resp.headers['Operation-Location']
    except KeyError:
        raise CLIError('Invalid response header key: Operation-Location')

    create_operation_status_id = operation_location.split('/')[(-1)]
    if verb:
        print ('Operation Id: {}').format(create_operation_status_id)
    operation_url = get_current_model_management_url_base() + MMS_OPERATION_URL_ENDPOINT.format(create_operation_status_id)
    operation_headers = {'Authorization': auth_header}
    sys.stdout.write('Updating service')
    sys.stdout.flush()
    service_id = poll_mms_async_operation(operation_url, operation_headers, params, MMS_SERVICE_CREATE_OPERATION_POLLING_MAX_TRIES, context)
    service_url = service_url + ('/{}').format(service_id)
    input_data = None
    try:
        resp = context.http_call('get', service_url, params=params, headers=headers, timeout=MMS_SYNC_TIMEOUT_SECONDS)
        if resp.status_code == 200:
            service = get_json(resp.content, pascal=True)
            scoring_url = service['ScoringUri']
            swagger_url = SWAGGER_URI_FORMAT.format(('/').join(scoring_url.split('/')[:-1]))
            keys_url = service_url + '/keys'
            keys_resp = context.http_call('get', keys_url, params=params, headers=headers, timeout=MMS_SYNC_TIMEOUT_SECONDS)
            if keys_resp.status_code == 200:
                service_keys = get_json(keys_resp.content, pascal=True)
                scoring_headers = {'Authorization': ('Bearer {}').format(service_keys['PrimaryKey'])}
                input_data = get_sample_data(swagger_url, headers=scoring_headers, verbose=verb)
            else:
                print 'Error occurred while attempting to get service swagger information.'
        else:
            print 'Error occurred while attempting to get service swagger information.'
    except (requests.ConnectionError, requests.Timeout, KeyError):
        print 'Error occurred while attempting to get service swagger information.'

    if not input_data:
        input_data = DEFAULT_INPUT_DATA
    print 'Done'
    print ('Service ID: {}').format(service_id)
    if context.os_is_unix():
        print ('Usage: az ml service run realtime -i {} -d {}').format(service_id, input_data)
    else:
        print ('Usage for cmd: az ml service run realtime -i {} -d {}').format(service_id, input_data)
        print ('Usage for powershell: az ml service run realtime -i {} --% -d {}').format(service_id, input_data)
    print ("Additional usage information: 'az ml service usage realtime -i {}'").format(service_id)
    return SUCCESS_RETURN_CODE


def mms_service_delete(service_id, verb, context):
    auth_header = get_auth_header()
    headers = {'Authorization': auth_header}
    params = {'api-version': MMS_API_VERSION}
    service_url = get_current_model_management_url_base() + MMS_SERVICE_URL_ENDPOINT + ('/{}').format(service_id)
    try:
        resp = context.http_call('delete', service_url, params=params, headers=headers, timeout=MMS_SYNC_TIMEOUT_SECONDS)
    except requests.ConnectionError:
        raise CLIError(('Error connecting to {}').format(service_url))
    except requests.Timeout:
        raise CLIError(('Error, request to {} timed out.').format(service_url))

    if resp.status_code == 200:
        print ('Successfully deleted service: {}').format(service_id)
        return SUCCESS_RETURN_CODE
    if resp.status_code == 204:
        print ('Service to delete {} not found.').format(service_id)
        return SUCCESS_RETURN_CODE
    raise CLIError(('Error occurred while attempting to delete service {}.\nStatus Code: {}\nHeaders: {}\nContent: {}').format(service_id, resp.status_code, resp.headers, resp.content))


def mms_service_list(verb, context):
    auth_header = get_auth_header()
    headers = {'Authorization': auth_header}
    params = {'api-version': MMS_API_VERSION}
    service_url = get_current_model_management_url_base() + MMS_SERVICE_URL_ENDPOINT
    try:
        resp = context.http_call('get', service_url, params=params, headers=headers, timeout=MMS_SYNC_TIMEOUT_SECONDS)
    except requests.ConnectionError:
        raise CLIError(('Error connecting to {}').format(service_url))
    except requests.Timeout:
        raise CLIError(('Error, request to {} timed out.').format(service_url))

    if resp.status_code == 200:
        return (SUCCESS_RETURN_CODE, get_paginated_results(resp, headers, context))
    raise CLIError(('Error occurred while attempting to list services.\nStatus Code: {}\nHeaders: {}\nContent: {}').format(resp.status_code, resp.headers, resp.content))


def mms_service_show(service_name, service_id, verb, context):
    auth_header = get_auth_header()
    headers = {'Authorization': auth_header}
    params = {'api-version': MMS_API_VERSION}
    service_url = get_current_model_management_url_base() + MMS_SERVICE_URL_ENDPOINT
    if service_name:
        params['serviceName'] = service_name
    else:
        service_url = service_url + ('/{}').format(service_id)
    try:
        resp = context.http_call('get', service_url, params=params, headers=headers, timeout=MMS_SYNC_TIMEOUT_SECONDS)
    except requests.ConnectionError:
        raise CLIError(('Error connecting to {}.').format(service_url))
    except requests.Timeout:
        raise CLIError(('Error, request to {} timed out.').format(service_url))

    if resp.status_code == 200:
        if service_name:
            result = get_paginated_results(resp, headers, context)
        else:
            result = get_json(resp.content, pascal=True)
    elif resp.status_code == 404 and service_id:
        result = None
    else:
        raise CLIError(('Error occurred while attempting to show service {}.\nStatus Code: {}\nHeaders: {}\nContent: {}').format(service_id, resp.status_code, resp.headers, resp.content))
    return (SUCCESS_RETURN_CODE, result)


def mms_service_keys_handling(service_id, regen, key, verb, context):
    auth_header = get_auth_header()
    headers = {'Content-Type': 'application/json', 'Authorization': auth_header}
    params = {'api-version': MMS_API_VERSION}
    if regen:
        if not key:
            raise CLIError('Error, must specify which key with be regenerated: Primary, Secondary')
        key = key.capitalize()
        if key != 'Primary' and key != 'Secondary':
            raise CLIError(('Error, invalid value provided for key: {}. Valid options are: Primary, Secondary').format(key))
        regen_keys_url = get_current_model_management_url_base() + MMS_SERVICE_REGEN_KEYS_URL_ENDPOINT.format(service_id)
        body = {'keyType': key}
        try:
            resp = context.http_call('post', regen_keys_url, params=params, headers=headers, json=body, timeout=MMS_SYNC_TIMEOUT_SECONDS)
        except requests.ConnectionError:
            raise CLIError(('Error connecting to {}.').format(regen_keys_url))
        except requests.Timeout:
            raise CLIError(('Error, request to {} timed out.').format(regen_keys_url))

    else:
        list_keys_url = get_current_model_management_url_base() + MMS_SERVICE_LIST_KEYS_URL_ENDPOINT.format(service_id)
        try:
            resp = context.http_call('get', list_keys_url, params=params, headers=headers, timeout=MMS_SYNC_TIMEOUT_SECONDS)
        except requests.ConnectionError:
            raise CLIError(('Error connecting to {}.').format(list_keys_url))
        except requests.Timeout:
            raise CLIError(('Error, request to {} timed out.').format(list_keys_url))

        if resp.status_code == 200:
            resp_obj = get_json(resp.content, pascal=True)
            try:
                primary_key = resp_obj['PrimaryKey']
            except KeyError:
                raise CLIError('Invalide response key: PrimaryKey')

            try:
                secondary_key = resp_obj['SecondaryKey']
            except KeyError:
                raise CLIError('Invalide response key: SecondaryKey')

            print ('PrimaryKey: {}\nSecondaryKey: {}').format(primary_key, secondary_key)
            return SUCCESS_RETURN_CODE
    if regen:
        action = 'regenerating'
    else:
        action = 'listing'
    raise CLIError(('Error occurred while {} keys for service.\nStatus Code: {}\nHeaders: {}\nContent: {}').format(action, resp.status_code, resp.headers, resp.content))


def mms_service_usage(service_id, verb, context):
    auth_header = get_auth_header()
    headers = {'Authorization': auth_header}
    params = {'api-version': MMS_API_VERSION}
    service_url = get_current_model_management_url_base() + MMS_SERVICE_URL_ENDPOINT + ('/{}').format(service_id)
    try:
        resp = context.http_call('get', service_url, params=params, headers=headers, timeout=MMS_SYNC_TIMEOUT_SECONDS)
    except requests.ConnectionError:
        raise CLIError(('Error connecting to {}.').format(service_url))
    except requests.Timeout:
        raise CLIError(('Error, request to {} timed out.').format(service_url))

    app_insights_url = None
    if resp.status_code == 200:
        service = get_json(resp.content, pascal=True)
        try:
            state = service['State']
            scoring_url = service['ScoringUri']
            if state != 'Succeeded' or not scoring_url:
                raise CLIError(('Error, service deployment is not succeeded, please check the status of your service.\nStatus Code: {}\nHeaders: {}\nContent: {}').format(resp.status_code, resp.headers, resp.content))
            swagger_url = SWAGGER_URI_FORMAT.format(('/').join(scoring_url.split('/')[:-1]))
            try:
                compute_params = {'api-version': MLC_API_VERSION}
                compute_resp = context.http_call('get', ('https://management.azure.com{}').format(service['ComputeResource']['Id']), params=compute_params, headers=headers, timeout=MMS_SYNC_TIMEOUT_SECONDS)
                if compute_resp.status_code == 200:
                    compute = get_json(compute_resp.content, pascal=True)
                    if 'Properties' in compute and 'AppInsights' in compute['Properties'] and compute['Properties']['AppInsights'] and 'ResourceId' in compute['Properties']['AppInsights']:
                        app_insights_resource_id = compute['Properties']['AppInsights']['ResourceId'].lstrip('/').split('/')
                        app_insights_url = APP_INSIGHTS_URL.format(app_insights_resource_id[1], app_insights_resource_id[3], app_insights_resource_id[(-1)])
            except (requests.ConnectionError, requests.Timeout, KeyError, AttributeError) as e:
                pass

        except KeyError:
            raise CLIError(('Error, unable to retrieve ScoringUri.\nStatus Code: {}\nHeaders: {}\nContent: {}').format(resp.status_code, resp.headers, resp.content))
        except AttributeError:
            raise CLIError(('Error, unable to retrieve swagger location.\nStatus Code: {}\nHeaders: {}\nContent: {}').format(resp.status_code, resp.headers, resp.content))

    else:
        raise CLIError(('Error occurred while attempting to retrieve service information.\nStatus Code: {}\nHeaders: {}\nContent: {}').format(resp.status_code, resp.headers, resp.content))
    scoring_headers = None
    try:
        keys_url = service_url + '/keys'
        keys_resp = context.http_call('get', keys_url, params=params, headers=headers, timeout=MMS_SYNC_TIMEOUT_SECONDS)
        if keys_resp.status_code == 200:
            service_keys = get_json(keys_resp.content, pascal=True)
            scoring_headers = {'Authorization': ('Bearer {}').format(service_keys['PrimaryKey'])}
        else:
            print 'Error occurred while attempting to get service swagger information.'
    except requests.ConnectionError:
        print 'Error occurred while attempting to get service swagger information.'
    except requests.Timeout:
        print 'Error occurred while attempting to get service swagger information.'

    return (scoring_url, swagger_url, scoring_headers, app_insights_url)


def mms_service_logs(service_id, request_id, kube_config, verb, context):
    if not service_id:
        raise CLIError('Error, service id required for cluster services.')
    default_kube_path = os.path.join(os.path.expanduser('~'), '.kube', 'config')
    if kube_config is None:
        if os.path.exists(default_kube_path):
            if verb:
                print ('Found default kubeconfig in {0} using it').format(default_kube_path)
            kube_config = default_kube_path
        else:
            raise CLIError('Kubeconfig needs to be provided to get logs in cluster mode. You can the following command to get it:az ml env get-credntials -g <resource group> -n <cluster name> -i')
    if verb:
        print ('Using kubeconfig file: {0}').format(kube_config)
    if not check_for_kubectl(context, verb=verb):
        print ''
        raise CLIError('kubectl is required to get logs from webservices. Please install it on your path and try again.')
    get_logs_from_kubernetes(service_id, kube_config, context, requestId=request_id, verb=verb)
    return SUCCESS_RETURN_CODE