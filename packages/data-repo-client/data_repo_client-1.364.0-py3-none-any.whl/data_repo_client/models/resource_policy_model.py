# coding: utf-8

"""
    Data Repository API

    <details><summary>This document defines the REST API for the Terra Data Repository.</summary> <p> **Status: design in progress** There are a few top-level endpoints (besides some used by swagger):  * / - generated by swagger: swagger API page that provides this documentation and a live UI for submitting REST requests  * /status - provides the operational status of the service  * /configuration - provides the basic configuration and information about the service  * /api - is the authenticated and authorized Data Repository API  * /ga4gh/drs/v1 - is a transcription of the Data Repository Service API  The API endpoints are organized by interface. Each interface is separately versioned. <p> **Notes on Naming** <p> All of the reference items are suffixed with \\\"Model\\\". Those names are used as the class names in the generated Java code. It is helpful to distinguish these model classes from other related classes, like the DAO classes and the operation classes. </details>   # noqa: E501

    The version of the OpenAPI document: 0.1.0
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from data_repo_client.configuration import Configuration


class ResourcePolicyModel(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'policy_email': 'str',
        'policy_name': 'str',
        'resource_id': 'str',
        'resource_type_name': 'str'
    }

    attribute_map = {
        'policy_email': 'policyEmail',
        'policy_name': 'policyName',
        'resource_id': 'resourceId',
        'resource_type_name': 'resourceTypeName'
    }

    def __init__(self, policy_email=None, policy_name=None, resource_id=None, resource_type_name=None, local_vars_configuration=None):  # noqa: E501
        """ResourcePolicyModel - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._policy_email = None
        self._policy_name = None
        self._resource_id = None
        self._resource_type_name = None
        self.discriminator = None

        if policy_email is not None:
            self.policy_email = policy_email
        if policy_name is not None:
            self.policy_name = policy_name
        if resource_id is not None:
            self.resource_id = resource_id
        if resource_type_name is not None:
            self.resource_type_name = resource_type_name

    @property
    def policy_email(self):
        """Gets the policy_email of this ResourcePolicyModel.  # noqa: E501


        :return: The policy_email of this ResourcePolicyModel.  # noqa: E501
        :rtype: str
        """
        return self._policy_email

    @policy_email.setter
    def policy_email(self, policy_email):
        """Sets the policy_email of this ResourcePolicyModel.


        :param policy_email: The policy_email of this ResourcePolicyModel.  # noqa: E501
        :type: str
        """

        self._policy_email = policy_email

    @property
    def policy_name(self):
        """Gets the policy_name of this ResourcePolicyModel.  # noqa: E501


        :return: The policy_name of this ResourcePolicyModel.  # noqa: E501
        :rtype: str
        """
        return self._policy_name

    @policy_name.setter
    def policy_name(self, policy_name):
        """Sets the policy_name of this ResourcePolicyModel.


        :param policy_name: The policy_name of this ResourcePolicyModel.  # noqa: E501
        :type: str
        """

        self._policy_name = policy_name

    @property
    def resource_id(self):
        """Gets the resource_id of this ResourcePolicyModel.  # noqa: E501

        Unique identifier for a dataset, snapshot, etc.   # noqa: E501

        :return: The resource_id of this ResourcePolicyModel.  # noqa: E501
        :rtype: str
        """
        return self._resource_id

    @resource_id.setter
    def resource_id(self, resource_id):
        """Sets the resource_id of this ResourcePolicyModel.

        Unique identifier for a dataset, snapshot, etc.   # noqa: E501

        :param resource_id: The resource_id of this ResourcePolicyModel.  # noqa: E501
        :type: str
        """

        self._resource_id = resource_id

    @property
    def resource_type_name(self):
        """Gets the resource_type_name of this ResourcePolicyModel.  # noqa: E501


        :return: The resource_type_name of this ResourcePolicyModel.  # noqa: E501
        :rtype: str
        """
        return self._resource_type_name

    @resource_type_name.setter
    def resource_type_name(self, resource_type_name):
        """Sets the resource_type_name of this ResourcePolicyModel.


        :param resource_type_name: The resource_type_name of this ResourcePolicyModel.  # noqa: E501
        :type: str
        """

        self._resource_type_name = resource_type_name

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
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

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, ResourcePolicyModel):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ResourcePolicyModel):
            return True

        return self.to_dict() != other.to_dict()
