# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ynab_api/api/user_api.py
# Compiled at: 2019-11-21 19:08:24
# Size of source mod 2**32: 5216 bytes
"""
    YNAB API Endpoints

    Our API uses a REST based design, leverages the JSON data format, and relies upon HTTPS for transport. We respond with meaningful HTTP response codes and if an error occurs, we include error details in the response body.  API Documentation is at https://api.youneedabudget.com  # noqa: E501

    The version of the OpenAPI document: 1.0.0
    Generated by: https://openapi-generator.tech
"""
from __future__ import absolute_import
import re, six
from ynab_api.api_client import ApiClient
from ynab_api.exceptions import ApiTypeError, ApiValueError

class UserApi(object):
    __doc__ = 'NOTE: This class is auto generated by OpenAPI Generator\n    Ref: https://openapi-generator.tech\n\n    Do not edit the class manually.\n    '

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def get_user(self, **kwargs):
        """User info  # noqa: E501

        Returns authenticated user information  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_user(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: UserResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return (self.get_user_with_http_info)(**kwargs)

    def get_user_with_http_info(self, **kwargs):
        """User info  # noqa: E501

        Returns authenticated user information  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_user_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(UserResponse, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """
        local_var_params = locals()
        all_params = []
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')
        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError("Got an unexpected keyword argument '%s' to method get_user" % key)
            local_var_params[key] = val

        del local_var_params['kwargs']
        collection_formats = {}
        path_params = {}
        query_params = []
        header_params = {}
        form_params = []
        local_var_files = {}
        body_params = None
        header_params['Accept'] = self.api_client.select_header_accept([
         'application/json'])
        auth_settings = [
         'bearer']
        return self.api_client.call_api('/user',
          'GET', path_params,
          query_params,
          header_params,
          body=body_params,
          post_params=form_params,
          files=local_var_files,
          response_type='UserResponse',
          auth_settings=auth_settings,
          async_req=(local_var_params.get('async_req')),
          _return_http_data_only=(local_var_params.get('_return_http_data_only')),
          _preload_content=(local_var_params.get('_preload_content', True)),
          _request_timeout=(local_var_params.get('_request_timeout')),
          collection_formats=collection_formats)