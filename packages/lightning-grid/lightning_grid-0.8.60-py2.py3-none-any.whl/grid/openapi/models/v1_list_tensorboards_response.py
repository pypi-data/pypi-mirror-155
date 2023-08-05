# coding: utf-8

"""
    external/v1/external_session_service.proto

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: version not set
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git

    NOTE
    ----
    standard swagger-codegen-cli for this python client has been modified
    by custom templates. The purpose of these templates is to include
    typing information in the API and Model code. Please refer to the
    main grid repository for more info
"""


import pprint
import re  # noqa: F401
from typing import TYPE_CHECKING

import six

from grid.openapi.configuration import Configuration

if TYPE_CHECKING:
    from datetime import datetime
    from grid.openapi.models import *

class V1ListTensorboardsResponse(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'next_page_token': 'str',
        'previous_page_token': 'str',
        'tensorboards': 'list[Externalv1Tensorboard]'
    }

    attribute_map = {
        'next_page_token': 'nextPageToken',
        'previous_page_token': 'previousPageToken',
        'tensorboards': 'tensorboards'
    }

    def __init__(self, next_page_token: 'str' = None, previous_page_token: 'str' = None, tensorboards: 'list[Externalv1Tensorboard]' = None, _configuration=None):  # noqa: E501
        """V1ListTensorboardsResponse - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._next_page_token = None
        self._previous_page_token = None
        self._tensorboards = None
        self.discriminator = None

        if next_page_token is not None:
            self.next_page_token = next_page_token
        if previous_page_token is not None:
            self.previous_page_token = previous_page_token
        if tensorboards is not None:
            self.tensorboards = tensorboards

    @property
    def next_page_token(self) -> 'str':
        """Gets the next_page_token of this V1ListTensorboardsResponse.  # noqa: E501


        :return: The next_page_token of this V1ListTensorboardsResponse.  # noqa: E501
        :rtype: str
        """
        return self._next_page_token

    @next_page_token.setter
    def next_page_token(self, next_page_token: 'str'):
        """Sets the next_page_token of this V1ListTensorboardsResponse.


        :param next_page_token: The next_page_token of this V1ListTensorboardsResponse.  # noqa: E501
        :type: str
        """

        self._next_page_token = next_page_token

    @property
    def previous_page_token(self) -> 'str':
        """Gets the previous_page_token of this V1ListTensorboardsResponse.  # noqa: E501


        :return: The previous_page_token of this V1ListTensorboardsResponse.  # noqa: E501
        :rtype: str
        """
        return self._previous_page_token

    @previous_page_token.setter
    def previous_page_token(self, previous_page_token: 'str'):
        """Sets the previous_page_token of this V1ListTensorboardsResponse.


        :param previous_page_token: The previous_page_token of this V1ListTensorboardsResponse.  # noqa: E501
        :type: str
        """

        self._previous_page_token = previous_page_token

    @property
    def tensorboards(self) -> 'list[Externalv1Tensorboard]':
        """Gets the tensorboards of this V1ListTensorboardsResponse.  # noqa: E501


        :return: The tensorboards of this V1ListTensorboardsResponse.  # noqa: E501
        :rtype: list[Externalv1Tensorboard]
        """
        return self._tensorboards

    @tensorboards.setter
    def tensorboards(self, tensorboards: 'list[Externalv1Tensorboard]'):
        """Sets the tensorboards of this V1ListTensorboardsResponse.


        :param tensorboards: The tensorboards of this V1ListTensorboardsResponse.  # noqa: E501
        :type: list[Externalv1Tensorboard]
        """

        self._tensorboards = tensorboards

    def to_dict(self) -> dict:
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(V1ListTensorboardsResponse, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self) -> str:
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self) -> str:
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other: 'V1ListTensorboardsResponse') -> bool:
        """Returns true if both objects are equal"""
        if not isinstance(other, V1ListTensorboardsResponse):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other: 'V1ListTensorboardsResponse') -> bool:
        """Returns true if both objects are not equal"""
        if not isinstance(other, V1ListTensorboardsResponse):
            return True

        return self.to_dict() != other.to_dict()
