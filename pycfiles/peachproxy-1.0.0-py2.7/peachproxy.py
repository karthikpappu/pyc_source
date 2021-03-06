# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\peachproxy.py
# Compiled at: 2017-03-15 13:57:55
"""Peach Proxy Python Module
Copyright (c) 2017 Peach API Security, LLC

This is a python module that provides method to call
the Peach Proxy Restful API.  This allows users
to integrate into unit-tests or custom traffic generators.
"""
from __future__ import print_function
import os, warnings, logging, requests, json, sys
from requests import put, get, delete, post
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logFormatter = logging.Formatter('%(asctime)s [%(levelname)-5.5s] %(message)s')
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
logger.addHandler(consoleHandler)
session = requests.Session()
session.trust_env = False
__peach_session = None
__peach_api = None
__peach_state = 'Continue'
__peach_proxy = None
__peach_ca_cert = None
__peach_api_token = None
__peach_api_token_field = 'Authorization'
__peach_headers = {}

def state():
    """Current state of Peach Proxy
    """
    global __peach_state
    return __peach_state


def session_id():
    """Get the current sessions id
    """
    global __peach_session
    return __peach_session['Id']


def set_session_id(session_id):
    """Get the current sessions id
    """
    global __peach_session
    if __peach_session == None:
        __peach_session = {}
    __peach_session['Id'] = session_id
    return


def proxy_ca_cert():
    """Get the current sessions proxy CA cert file
    """
    global __peach_ca_cert
    return __peach_ca_cert


def set_proxy_ca_cert(filename):
    """Set the current sessions proxy CA cert file
    """
    global __peach_ca_cert
    __peach_ca_cert = filename


def proxy_url():
    """Get the current sessions proxy url
    """
    return __peach_session['ProxyUrl']


def set_proxy_url(url):
    """Get the current sessions proxy url
    """
    global __peach_session
    if __peach_session == None:
        __peach_session = {}
    __peach_session['ProxyUrl'] = url
    return


def set_peach_api(api):
    """Get the current sessions proxy url
    """
    global __peach_api
    __peach_api = api


def get_peach_api_token():
    """Get Peach API Token
    """
    global __peach_api_token
    return __peach_api_token


def set_peach_api_token(token):
    """Set Peach API token.

    This token can be found on the Settings page of the
    Peach API Security product.
    """
    global __peach_api_token
    global __peach_api_token_field
    global __peach_headers
    __peach_api_token = token
    __peach_headers = {__peach_api_token_field: 'Token ' + __peach_api_token}


arg = os.environ.get('PEACH_API', None)
if arg != None:
    set_peach_api(arg)
arg = os.environ.get('PEACH_API_TOKEN', None)
if arg != None:
    set_peach_api_token(arg)
arg = os.environ.get('PEACH_SESSIONID', None)
if arg != None:
    set_session_id(arg)
arg = os.environ.get('PEACH_PROXY', None)
if arg != None:
    set_proxy_url(arg)
arg = os.environ.get('PEACH_CA_CERT', None)
if arg != None:
    set_proxy_ca_cert(arg)

def get_jobs():
    """Get list of job summaries
    """
    logger.debug('>>get_jobs')
    if not __peach_api:
        logger.error('Called session_setup() w/o a peach_api url')
        sys.exit(-1)
    if not __peach_api_token:
        logger.error('Called session_setup() w/o a peach_api_token')
        sys.exit(-1)
    try:
        r = session.get('%s/api/jobs' % __peach_api, headers=__peach_headers)
        if r.status_code != 200:
            logger.error('Error calling /api/jobs: %s %s', r.status_code, r.reason)
            sys.exit(-1)
        return r.json()
    except requests.exceptions.RequestException as e:
        logger.error('Error communicating with Peach API Security.')
        logger.error('vvvv ERROR vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv')
        logger.error(e)
        logger.error('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
        sys.exit(-1)


def stop_job(id):
    """Stop a job

    Keyword arguments:
    id -- Job/Session id
    """
    logger.debug('>>stop_job(%s)', id)
    try:
        orig_session_id = session_id()
    except:
        orig_session_id = None

    set_session_id(id)
    try:
        session_teardown()
    finally:
        set_session_id(orig_session_id)

    return


def session_setup(project, profile, api):
    """Notify Peach Proxy that a test session is starting.
    Called ONCE at start of testing.

    Keyword arguments:
    project -- Configuration to launch
    profile -- Name of profile within project to launch
    api -- Peach API URL, example: http://127.0.0.1:5000
    """
    global __peach_api
    global __peach_session
    logger.debug('>>session_setup')
    if not __peach_api:
        logger.error('Called session_setup() w/o a peach_api url')
        sys.exit(-1)
    if not __peach_api_token:
        logger.error('Called session_setup() w/o a peach_api_token')
        sys.exit(-1)
    __peach_api = api
    try:
        params = {'project': project, 
           'profile': profile}
        r = session.post('%s/api/sessions' % api, params=params, headers=__peach_headers)
        if r.status_code != 201:
            logger.error('Error calling /api/sessions: %s %s', r.status_code, r.reason)
            sys.exit(-1)
        __peach_session = r.json()
        logger.info('Peach API Security Version: %s', r.headers['X-Peach-Version'])
        logger.info('Session ID: %s', session_id())
        logger.info('Proxy URL: %s', proxy_url())
        certfile = proxy_ca_cert()
        if certfile:
            with open(certfile, 'w') as (f):
                f.write(__peach_session['Certificate'])
            logger.info('CA Cert: %s', certfile)
        verify_proxy_access()
    except requests.exceptions.RequestException as e:
        logger.error('Error communicating with Peach API Security.')
        logger.error('vvvv ERROR vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv')
        logger.error(e)
        logger.error('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
        sys.exit(-1)


def verify_proxy_access():
    """Make a ping request through proxy port to verify proxy access

    Verify connectivity to the Peach API Security proxy port.
    """
    logger.debug('>>verify_proxy_access')
    if not __peach_session:
        logger.error('Called verify_proxy_access() w/o a session id')
        sys.exit(-1)
    try:
        r = session.get(proxy_url(), headers={'X-PeachProxy-Probe': 'peachproxy'})
        if r.status_code != 200:
            logger.error('Error verifying proxy port, incorrect status code via %s: %s', (
             proxy_url(), r.status_code))
            logger.error('Please verify correct access to %s. This error is typically')
            logger.error('due to incorrect deployment of Peach API Security or network issues.')
            sys.exit(-1)
        try:
            data = r.json()
            if not data['ping'] == 'pong':
                raise Exception()
        except:
            logger.error('Error verifying proxy port, incorrect body returned via %s', proxy_url())
            logger.error('Unexpected Body: %s', r.text)
            logger.error('Please verify correct access to %s. This error is typically', proxy_url())
            logger.error('due to incorrect deployment of Peach API Security or network issues.')
            logger.error('Verify no HTTP proxies are inbetween you and Peach API Security.')
            sys.exit(-1)

    except requests.exceptions.RequestException as e:
        logger.error('Error validating access to Peach API Security proxy port.')
        logger.error('Please verify correct access to %s. This error is typically')
        logger.error('due to incorrect deployment of Peach API Security or a network issue.')
        logger.error('Verify access to the port in this URL: %s', proxy_url())
        sys.exit(-1)


def session_teardown():
    """Notify Peach Proxy that a test session is ending.

    Called ONCE at end of testing. This will cause Peach to stop.
    
    Returns:
        bool: True says failures found during testing
              False says testing completed without issue
    """
    logger.debug('>>session_teardown')
    if not __peach_session:
        logger.error('Called session_teardown() w/o a session id')
        sys.exit(-1)
    if not __peach_api:
        logger.error('Called session_teardown() w/o a peach_api url')
        sys.exit(-1)
    if not __peach_api_token:
        logger.error('Called session_teardown() w/o a peach_api_token')
        sys.exit(-1)
    try:
        r = session.delete('%s/api/sessions/%s' % (__peach_api, session_id()), headers=__peach_headers)
        if r.status_code != 200:
            logger.error('Error deleting session via /api/sessions/id: %s', r.status_code)
            sys.exit(-1)
        r = r.json()
        return bool(r['HasFaults'])
    except requests.exceptions.RequestException as e:
        logger.error('Error communicating with Peach API Security.')
        logger.error('vvvv ERROR vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv')
        logger.error(e)
        logger.error('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
        sys.exit(-1)


def session_state():
    """Return the job state

        - Invalid (should never be here)
        - Running - testing is in progress
        - Idle - testing has completed
        - Error - non recoverable error has occured
        - Finished - State post-session_teardown
    """
    logger.debug('>>session_state')
    if not __peach_session:
        logger.error('Called session_state() w/o a session id')
        sys.exit(-1)
    if not __peach_api:
        logger.error('Called session_state() w/o a peach_api url')
        sys.exit(-1)
    if not __peach_api_token:
        logger.error('Called session_state() w/o a peach_api_token')
        sys.exit(-1)
    try:
        r = session.get('%s/api/sessions/%s' % (__peach_api, session_id()), headers=__peach_headers)
        if r.status_code != 200:
            logger.error('Error getting session state via /api/sessions/id: %s', r.status_code)
            sys.exit(-1)
        r = r.json()
        return r['State']
    except requests.exceptions.RequestException as e:
        logger.error('Error communicating with Peach API Security.')
        logger.error('vvvv ERROR vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv')
        logger.error(e)
        logger.error('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
        sys.exit(-1)


def session_error_reason():
    """Return any error message associated with job.
    """
    logger.debug('>>session_error_reason')
    if not __peach_session:
        logger.error('Called session_error_reason() w/o a session id')
        sys.exit(-1)
    if not __peach_api:
        logger.error('Called session_error_reason() w/o a peach_api url')
        sys.exit(-1)
    if not __peach_api_token:
        logger.error('Called session_error_reason() w/o a peach_api_token')
        sys.exit(-1)
    try:
        r = session.get('%s/api/sessions/%s' % (__peach_api, session_id()), headers=__peach_headers)
        if r.status_code != 200:
            logger.error('Error getting session error reason via /api/sessions/id: %s', r.status_code)
            sys.exit(-1)
        r = r.json()
        return r['Reason']
    except requests.exceptions.RequestException as e:
        logger.error('Error communicating with Peach API Security.')
        logger.error('vvvv ERROR vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv')
        logger.error(e)
        logger.error('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
        sys.exit(-1)


def setup():
    """Notify Peach Proxy that setup tasks are about to run.

    This will disable fuzzing of messages so the setup tasks
    always work OK.
    """
    logger.debug('>>setup()')
    if not __peach_session:
        logger.error('Called setup() w/o a session id')
        sys.exit(-1)
    if not __peach_api:
        logger.error('Called setup() w/o a peach_api url')
        sys.exit(-1)
    if not __peach_api_token:
        logger.error('Called setup() w/o a peach_api_token')
        sys.exit(-1)
    try:
        r = session.post('%s/api/sessions/%s/TestSetUp' % (__peach_api, session_id()), headers=__peach_headers)
        if r.status_code != 200:
            logger.error("Error sending TestSetUp for session '%s': %s %s", session_id(), r.status_code, r.reason)
            sys.exit(-1)
    except requests.exceptions.RequestException as e:
        logger.error('Error communicating with Peach API Security.')
        logger.error('vvvv ERROR vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv')
        logger.error(e)
        logger.error('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
        sys.exit(-1)


def teardown():
    """Notify Peach Proxy that teardown tasks are about to run.

    This will disable fuzzing of messages so the teardown tasks
    always work OK.
    
    Returns:
        str: Returns a string indicating next action
             Continue - Produce another of the current test case,
             NextTest - Move to next test case if any
             Error - Non-recoverable error has occurred. Exit.
    """
    global __peach_state
    logger.debug('>>teardown')
    if not __peach_session:
        logger.error('Called teardown() w/o a session id')
        sys.exit(-1)
    if not __peach_api:
        logger.error('Called teardown() w/o a peach_api url')
        sys.exit(-1)
    if not __peach_api_token:
        logger.error('Called teardown() w/o a peach_api_token')
        sys.exit(-1)
    try:
        r = session.post('%s/api/sessions/%s/TestTearDown' % (__peach_api, session_id()), headers=__peach_headers)
        if r.status_code != 200:
            logger.error('Error sending TestTearDown: %s', r.status_code)
            sys.exit(-1)
        __peach_state = str(r.json())
        logger.debug('<<teardown: state: %s', __peach_state)
        return __peach_state
    except requests.exceptions.RequestException as e:
        logger.error('Error communicating with Peach API Security.')
        logger.error('vvvv ERROR vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv')
        logger.error(e)
        logger.error('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
        sys.exit(-1)


def suite_teardown():
    """Notify Peach that traffic generator has completed

    Normally this is called once the result of teardown() has indicate
    Peach has finished testing.  However, in the case that the
    traffic generator encounters a non-recoverable error,
    suite_teardown() will cause the Peach Job to error.
    """
    logger.debug('>>suite_teardown')
    if not __peach_session:
        logger.error('Called suite_teardown() w/o a session id')
        sys.exit(-1)
    if not __peach_api:
        logger.error('Called suite_teardown() w/o a peach_api url')
        sys.exit(-1)
    if not __peach_api_token:
        logger.error('Called suite_teardown() w/o a peach_api_token')
        sys.exit(-1)
    try:
        r = session.post('%s/api/sessions/%s/TestSuiteTearDown' % (__peach_api, session_id()), headers=__peach_headers)
        if r.status_code != 200:
            logger.error('Error sending TestSuiteTearDown: %s', r.status_code)
            sys.exit(-1)
    except requests.exceptions.RequestException as e:
        logger.error('Error communicating with Peach API Security.')
        logger.error('vvvv ERROR vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv')
        logger.error(e)
        logger.error('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
        sys.exit(-1)


def testcase(name):
    """Notify Peach Proxy that a test case is starting.
    This will enable fuzzing and group all of the following
    requests into a group.

    Keyword arguments:
    name -- Name of unit test. Shows up in metrics.
    """
    logger.debug('>>testcase(%s)', name)
    if not __peach_session:
        logger.error('Called testcase() w/o a session id')
        sys.exit(-1)
    if not __peach_api:
        logger.error('Called testcase() w/o a peach_api')
        sys.exit(-1)
    if not __peach_api_token:
        logger.error('Called testcase() w/o a peach_api_token')
        sys.exit(-1)
    try:
        r = session.post('%s/api/sessions/%s/testRun?name=%s' % (__peach_api, session_id(), name), headers=__peach_headers)
        if r.status_code != 200:
            logger.error('Error sending testRun: %s', r.status_code)
            sys.exit(-1)
    except requests.exceptions.RequestException as e:
        logger.error('Error communicating with Peach API Security.')
        logger.error('vvvv ERROR vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv')
        logger.error(e)
        logger.error('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
        sys.exit(-1)


def junit_xml():
    """Generate JUnit style XML output for use with CI integration.
    """
    logger.debug('>>junit_xml')
    if not __peach_session:
        logger.error('Called junit_xml() w/o a session id')
        sys.exit(-1)
    if not __peach_api:
        logger.error('Called junit_xml() w/o a peach_api')
        sys.exit(-1)
    if not __peach_api_token:
        logger.error('Called junit_xml() w/o a peach_api_token')
        sys.exit(-1)
    try:
        r = session.get('%s/api/jobs/%s/junit' % (__peach_api, session_id()), headers=__peach_headers)
        if r.status_code != 200:
            logger.error('Error sending testRun: %s', r.status_code)
            sys.exit(-1)
        return r.text
    except requests.exceptions.RequestException as e:
        logger.error('Error communicating with Peach API Security.')
        logger.error('vvvv ERROR vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv')
        logger.error(e)
        logger.error('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
        sys.exit(-1)


def get_faults(job_id):
    """Get list of job summaries
    """
    logger.debug('>>get_jobs(%s)' % job_id)
    if not __peach_api:
        logger.error('Called session_setup() w/o a peach_api url')
        sys.exit(-1)
    if not __peach_api_token:
        logger.error('Called session_setup() w/o a peach_api_token')
        sys.exit(-1)
    try:
        r = session.get('%s/api/jobs/%s/faults' % (__peach_api, job_id), headers=__peach_headers)
        if r.status_code != 200:
            logger.error('Error calling /api/jobs/%s/faults: %s %s', job_id, r.status_code, r.reason)
            sys.exit(-1)
        return r.json()
    except requests.exceptions.RequestException as e:
        logger.error('Error communicating with Peach API Security.')
        logger.error('vvvv ERROR vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv')
        logger.error(e)
        logger.error('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
        sys.exit(-1)


def get_fault(job_id, fault_id):
    """Get list of job summaries
    """
    logger.debug('>>get_jobs(%s)' % job_id)
    if not __peach_api:
        logger.error('Called session_setup() w/o a peach_api url')
        sys.exit(-1)
    if not __peach_api_token:
        logger.error('Called session_setup() w/o a peach_api_token')
        sys.exit(-1)
    try:
        r = session.get('%s/api/jobs/%s/faults/%s' % (__peach_api, job_id, fault_id), headers=__peach_headers)
        if r.status_code != 200:
            logger.error('Error calling /api/jobs/%s/faults/%s: %s %s', job_id, fault_id, r.status_code, r.reason)
            sys.exit(-1)
        return r.json()
    except requests.exceptions.RequestException as e:
        logger.error('Error communicating with Peach API Security.')
        logger.error('vvvv ERROR vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv')
        logger.error(e)
        logger.error('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
        sys.exit(-1)


if __name__ == '__main__':
    print('This is a python module and should only be used by other')
    print('Python programs.  It was not intended to be run directly.')
    print('\n')
    print('For more information see the README')