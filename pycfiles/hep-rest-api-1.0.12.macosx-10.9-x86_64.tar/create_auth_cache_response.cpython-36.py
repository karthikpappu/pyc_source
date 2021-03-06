# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/erhu/project/gitrepo/hep-sdk/venv/lib/python3.6/site-packages/hep_rest_api/models/create_auth_cache_response.py
# Compiled at: 2019-07-15 09:20:14
# Size of source mod 2**32: 3602 bytes
"""
    HEP REST API

    The REST API for HEP protocol  # noqa: E501

    OpenAPI spec version: v1
    Contact: xiawu@zeuux.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""
import pprint, re, six

class CreateAuthCacheResponse(object):
    __doc__ = 'NOTE: This class is auto generated by the swagger code generator program.\n\n    Do not edit the class manually.\n    '
    swagger_types = {'auth_hash': 'str'}
    attribute_map = {'auth_hash': 'auth_hash'}

    def __init__(self, auth_hash=None):
        """CreateAuthCacheResponse - a model defined in Swagger"""
        self._auth_hash = None
        self.discriminator = None
        self.auth_hash = auth_hash

    @property
    def auth_hash(self):
        """Gets the auth_hash of this CreateAuthCacheResponse.  # noqa: E501

        :return: The auth_hash of this CreateAuthCacheResponse.  # noqa: E501
        :rtype: str
        """
        return self._auth_hash

    @auth_hash.setter
    def auth_hash(self, auth_hash):
        """Sets the auth_hash of this CreateAuthCacheResponse.

        :param auth_hash: The auth_hash of this CreateAuthCacheResponse.  # noqa: E501
        :type: str
        """
        if auth_hash is None:
            raise ValueError('Invalid value for `auth_hash`, must not be `None`')
        else:
            if auth_hash is not None:
                if len(auth_hash) > 64:
                    raise ValueError('Invalid value for `auth_hash`, length must be less than or equal to `64`')
            if auth_hash is not None:
                if len(auth_hash) < 1:
                    raise ValueError('Invalid value for `auth_hash`, length must be greater than or equal to `1`')
        self._auth_hash = auth_hash

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}
        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(lambda x: x.to_dict() if hasattr(x, 'to_dict') else x, value))
            else:
                if hasattr(value, 'to_dict'):
                    result[attr] = value.to_dict()
                else:
                    if isinstance(value, dict):
                        result[attr] = dict(map(lambda item: (item[0], item[1].to_dict()) if hasattr(item[1], 'to_dict') else item, value.items()))
                    else:
                        result[attr] = value

        if issubclass(CreateAuthCacheResponse, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, CreateAuthCacheResponse):
            return False
        else:
            return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other