# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/mux_python/rest.py
# Compiled at: 2020-03-11 08:26:48
# Size of source mod 2**32: 14544 bytes
"""
Mux Python - Copyright 2019 Mux Inc.

NOTE: This class is auto generated. Do not edit the class manually.
"""
from __future__ import absolute_import
import io, json, logging, re, ssl, certifi, six
from six.moves.urllib.parse import urlencode
try:
    import urllib3
except ImportError:
    raise ImportError('OpenAPI Python client requires urllib3.')
else:
    logger = logging.getLogger(__name__)

    class RESTResponse(io.IOBase):

        def __init__(self, resp):
            self.urllib3_response = resp
            self.status = resp.status
            self.reason = resp.reason
            self.data = resp.data

        def getheaders(self):
            """Returns a dictionary of the response headers."""
            return self.urllib3_response.getheaders()

        def getheader(self, name, default=None):
            """Returns a given response header."""
            return self.urllib3_response.getheader(name, default)


    class RESTClientObject(object):

        def __init__(self, configuration, pools_size=4, maxsize=None):
            if configuration.verify_ssl:
                cert_reqs = ssl.CERT_REQUIRED
            else:
                cert_reqs = ssl.CERT_NONE
            if configuration.ssl_ca_cert:
                ca_certs = configuration.ssl_ca_cert
            else:
                ca_certs = certifi.where()
            addition_pool_args = {}
            if configuration.assert_hostname is not None:
                addition_pool_args['assert_hostname'] = configuration.assert_hostname
            else:
                if maxsize is None:
                    if configuration.connection_pool_maxsize is not None:
                        maxsize = configuration.connection_pool_maxsize
                    else:
                        maxsize = 4
                if configuration.proxy:
                    self.pool_manager = (urllib3.ProxyManager)(num_pools=pools_size, 
                     maxsize=maxsize, 
                     cert_reqs=cert_reqs, 
                     ca_certs=ca_certs, 
                     cert_file=configuration.cert_file, 
                     key_file=configuration.key_file, 
                     proxy_url=configuration.proxy, **addition_pool_args)
                else:
                    self.pool_manager = (urllib3.PoolManager)(num_pools=pools_size, 
                     maxsize=maxsize, 
                     cert_reqs=cert_reqs, 
                     ca_certs=ca_certs, 
                     cert_file=configuration.cert_file, 
                     key_file=configuration.key_file, **addition_pool_args)

        def request(self, method, url, query_params=None, headers=None, body=None, post_params=None, _preload_content=True, _request_timeout=None):
            """Perform requests.

        :param method: http request method
        :param url: http request url
        :param query_params: query parameters in the url
        :param headers: http request headers
        :param body: request json body, for `application/json`
        :param post_params: request post parameters,
                            `application/x-www-form-urlencoded`
                            and `multipart/form-data`
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        """
            method = method.upper()
            if not method in ('GET', 'HEAD', 'DELETE', 'POST', 'PUT', 'PATCH', 'OPTIONS'):
                raise AssertionError
            elif post_params:
                if body:
                    raise ValueError('body parameter cannot be used with post_params parameter.')
            else:
                post_params = post_params or {}
                headers = headers or {}
                timeout = None
                if _request_timeout:
                    if isinstance(_request_timeout, (int,) if six.PY3 else (int, long)):
                        timeout = urllib3.Timeout(total=_request_timeout)
                    else:
                        if isinstance(_request_timeout, tuple) and len(_request_timeout) == 2:
                            timeout = urllib3.Timeout(connect=(_request_timeout[0]),
                              read=(_request_timeout[1]))
            if 'Content-Type' not in headers:
                headers['Content-Type'] = 'application/json'
            try:
                if method in ('POST', 'PUT', 'PATCH', 'OPTIONS', 'DELETE'):
                    if query_params:
                        url += '?' + urlencode(query_params)
                    elif re.search('json', headers['Content-Type'], re.IGNORECASE):
                        request_body = None
                        if body is not None:
                            request_body = json.dumps(body)
                        r = self.pool_manager.request(method,
                          url, body=request_body,
                          preload_content=_preload_content,
                          timeout=timeout,
                          headers=headers)
                    else:
                        if headers['Content-Type'] == 'application/x-www-form-urlencoded':
                            r = self.pool_manager.request(method,
                              url, fields=post_params,
                              encode_multipart=False,
                              preload_content=_preload_content,
                              timeout=timeout,
                              headers=headers)
                        else:
                            if headers['Content-Type'] == 'multipart/form-data':
                                del headers['Content-Type']
                                r = self.pool_manager.request(method,
                                  url, fields=post_params,
                                  encode_multipart=True,
                                  preload_content=_preload_content,
                                  timeout=timeout,
                                  headers=headers)
                            else:
                                if isinstance(body, str):
                                    request_body = body
                                    r = self.pool_manager.request(method,
                                      url, body=request_body,
                                      preload_content=_preload_content,
                                      timeout=timeout,
                                      headers=headers)
                                else:
                                    msg = 'Cannot prepare a request message for provided\n                             arguments. Please check that your arguments match\n                             declared content type.'
                                    raise ApiException(status=0, reason=msg)
                else:
                    r = self.pool_manager.request(method, url, fields=query_params,
                      preload_content=_preload_content,
                      timeout=timeout,
                      headers=headers)
            except urllib3.exceptions.SSLError as e:
                try:
                    msg = '{0}\n{1}'.format(type(e).__name__, str(e))
                    raise ApiException(status=0, reason=msg)
                finally:
                    e = None
                    del e

            else:
                if _preload_content:
                    r = RESTResponse(r)
                    if six.PY3:
                        r.data = r.data.decode('utf8')
                    logger.debug('response body: %s', r.data)
                else:
                    if r.status == 401:
                        raise UnauthorizedException(http_resp=r)
                    if r.status == 403:
                        raise ForbiddenException(http_resp=r)
                    if r.status == 404:
                        raise NotFoundException(http_resp=r)
                    if 500 <= r.status <= 599:
                        raise ServiceException(http_resp=r)
                if not 200 <= r.status <= 299:
                    raise ApiException(http_resp=r)
                return r

        def GET(self, url, headers=None, query_params=None, _preload_content=True, _request_timeout=None):
            return self.request('GET', url, headers=headers,
              _preload_content=_preload_content,
              _request_timeout=_request_timeout,
              query_params=query_params)

        def HEAD(self, url, headers=None, query_params=None, _preload_content=True, _request_timeout=None):
            return self.request('HEAD', url, headers=headers,
              _preload_content=_preload_content,
              _request_timeout=_request_timeout,
              query_params=query_params)

        def OPTIONS(self, url, headers=None, query_params=None, post_params=None, body=None, _preload_content=True, _request_timeout=None):
            return self.request('OPTIONS', url, headers=headers,
              query_params=query_params,
              post_params=post_params,
              _preload_content=_preload_content,
              _request_timeout=_request_timeout,
              body=body)

        def DELETE(self, url, headers=None, query_params=None, body=None, _preload_content=True, _request_timeout=None):
            return self.request('DELETE', url, headers=headers,
              query_params=query_params,
              _preload_content=_preload_content,
              _request_timeout=_request_timeout,
              body=body)

        def POST(self, url, headers=None, query_params=None, post_params=None, body=None, _preload_content=True, _request_timeout=None):
            return self.request('POST', url, headers=headers,
              query_params=query_params,
              post_params=post_params,
              _preload_content=_preload_content,
              _request_timeout=_request_timeout,
              body=body)

        def PUT(self, url, headers=None, query_params=None, post_params=None, body=None, _preload_content=True, _request_timeout=None):
            return self.request('PUT', url, headers=headers,
              query_params=query_params,
              post_params=post_params,
              _preload_content=_preload_content,
              _request_timeout=_request_timeout,
              body=body)

        def PATCH(self, url, headers=None, query_params=None, post_params=None, body=None, _preload_content=True, _request_timeout=None):
            return self.request('PATCH', url, headers=headers,
              query_params=query_params,
              post_params=post_params,
              _preload_content=_preload_content,
              _request_timeout=_request_timeout,
              body=body)


    class ApiException(Exception):

        def __init__(self, status=None, reason=None, http_resp=None):
            if http_resp:
                self.status = http_resp.status
                self.reason = http_resp.reason
                self.body = http_resp.data
                self.headers = http_resp.getheaders()
                try:
                    error_response = json.loads(http_resp.data)
                    self.error_type = error_response['error']['type']
                    self.error_messages = error_response['error']['messages']
                except Exception as e:
                    try:
                        self.error_type = None
                        self.error_messages = None
                    finally:
                        e = None
                        del e

            else:
                self.status = status
                self.reason = reason
                self.body = None
                self.headers = None
                self.error_type = None
                self.error_messages = None

        def __str__(self):
            """Custom error messages for exception"""
            error_message = '({0})\nReason: {1}\n'.format(self.status, self.reason)
            if self.headers:
                error_message += 'HTTP response headers: {0}\n'.format(self.headers)
            if self.body:
                error_message += 'HTTP response body: {0}\n'.format(self.body)
            return error_message


    class NotFoundException(ApiException):

        def __init__(self, status=None, reason=None, http_resp=None):
            ApiException.__init__(self, status, reason, http_resp)


    class UnauthorizedException(ApiException):

        def __init__(self, status=None, reason=None, http_resp=None):
            ApiException.__init__(self, status, reason, http_resp)


    class ForbiddenException(ApiException):

        def __init__(self, status=None, reason=None, http_resp=None):
            ApiException.__init__(self, status, reason, http_resp)


    class ServiceException(ApiException):

        def __init__(self, status=None, reason=None, http_resp=None):
            ApiException.__init__(self, status, reason, http_resp)