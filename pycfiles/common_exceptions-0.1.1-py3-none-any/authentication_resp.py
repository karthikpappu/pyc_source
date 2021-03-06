# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/common_dibbs/clients/cas_client/models/authentication_resp.py
# Compiled at: 2016-12-14 11:02:41
__doc__ = '\n    Central authentication service API\n\n    Central authentication service via API.\n\n    OpenAPI spec version: 0.1.1\n    \n    Generated by: https://github.com/swagger-api/swagger-codegen.git\n\n    Licensed under the Apache License, Version 2.0 (the "License");\n    you may not use this file except in compliance with the License.\n    You may obtain a copy of the License at\n\n        http://www.apache.org/licenses/LICENSE-2.0\n\n    Unless required by applicable law or agreed to in writing, software\n    distributed under the License is distributed on an "AS IS" BASIS,\n    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n    See the License for the specific language governing permissions and\n    limitations under the License.\n'
from pprint import pformat
from six import iteritems
import re

class AuthenticationResp(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """

    def __init__(self, response=None, token=None):
        """
        AuthenticationResp - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {'response': 'bool', 
           'token': 'str'}
        self.attribute_map = {'response': 'response', 
           'token': 'token'}
        self._response = response
        self._token = token

    @property
    def response(self):
        """
        Gets the response of this AuthenticationResp.

        :return: The response of this AuthenticationResp.
        :rtype: bool
        """
        return self._response

    @response.setter
    def response(self, response):
        """
        Sets the response of this AuthenticationResp.

        :param response: The response of this AuthenticationResp.
        :type: bool
        """
        self._response = response

    @property
    def token(self):
        """
        Gets the token of this AuthenticationResp.

        :return: The token of this AuthenticationResp.
        :rtype: str
        """
        return self._token

    @token.setter
    def token(self, token):
        """
        Sets the token of this AuthenticationResp.

        :param token: The token of this AuthenticationResp.
        :type: str
        """
        self._token = token

    def to_dict(self):
        """
        Returns the model properties as a dict
        """
        result = {}
        for attr, _ in iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(lambda x: x.to_dict() if hasattr(x, 'to_dict') else x, value))
            elif hasattr(value, 'to_dict'):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(lambda item: (item[0], item[1].to_dict()) if hasattr(item[1], 'to_dict') else item, value.items()))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """
        Returns the string representation of the model
        """
        return pformat(self.to_dict())

    def __repr__(self):
        """
        For `print` and `pprint`
        """
        return self.to_str()

    def __eq__(self, other):
        """
        Returns true if both objects are equal
        """
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other