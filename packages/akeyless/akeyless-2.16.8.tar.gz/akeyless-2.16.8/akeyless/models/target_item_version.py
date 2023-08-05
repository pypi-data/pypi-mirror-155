# coding: utf-8

"""
    Akeyless API

    The purpose of this application is to provide access to Akeyless API.  # noqa: E501

    The version of the OpenAPI document: 2.0
    Contact: support@akeyless.io
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from akeyless.configuration import Configuration


class TargetItemVersion(object):
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
        'creation_date': 'datetime',
        'customer_fragment_id': 'str',
        'deletion_date': 'datetime',
        'item_version_state': 'str',
        'latest_version': 'bool',
        'protection_key_name': 'str',
        'target_name': 'str',
        'version': 'int',
        'with_customer_fragment': 'bool'
    }

    attribute_map = {
        'creation_date': 'creation_date',
        'customer_fragment_id': 'customer_fragment_id',
        'deletion_date': 'deletion_date',
        'item_version_state': 'item_version_state',
        'latest_version': 'latest_version',
        'protection_key_name': 'protection_key_name',
        'target_name': 'target_name',
        'version': 'version',
        'with_customer_fragment': 'with_customer_fragment'
    }

    def __init__(self, creation_date=None, customer_fragment_id=None, deletion_date=None, item_version_state=None, latest_version=None, protection_key_name=None, target_name=None, version=None, with_customer_fragment=None, local_vars_configuration=None):  # noqa: E501
        """TargetItemVersion - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._creation_date = None
        self._customer_fragment_id = None
        self._deletion_date = None
        self._item_version_state = None
        self._latest_version = None
        self._protection_key_name = None
        self._target_name = None
        self._version = None
        self._with_customer_fragment = None
        self.discriminator = None

        if creation_date is not None:
            self.creation_date = creation_date
        if customer_fragment_id is not None:
            self.customer_fragment_id = customer_fragment_id
        if deletion_date is not None:
            self.deletion_date = deletion_date
        if item_version_state is not None:
            self.item_version_state = item_version_state
        if latest_version is not None:
            self.latest_version = latest_version
        if protection_key_name is not None:
            self.protection_key_name = protection_key_name
        if target_name is not None:
            self.target_name = target_name
        if version is not None:
            self.version = version
        if with_customer_fragment is not None:
            self.with_customer_fragment = with_customer_fragment

    @property
    def creation_date(self):
        """Gets the creation_date of this TargetItemVersion.  # noqa: E501


        :return: The creation_date of this TargetItemVersion.  # noqa: E501
        :rtype: datetime
        """
        return self._creation_date

    @creation_date.setter
    def creation_date(self, creation_date):
        """Sets the creation_date of this TargetItemVersion.


        :param creation_date: The creation_date of this TargetItemVersion.  # noqa: E501
        :type: datetime
        """

        self._creation_date = creation_date

    @property
    def customer_fragment_id(self):
        """Gets the customer_fragment_id of this TargetItemVersion.  # noqa: E501


        :return: The customer_fragment_id of this TargetItemVersion.  # noqa: E501
        :rtype: str
        """
        return self._customer_fragment_id

    @customer_fragment_id.setter
    def customer_fragment_id(self, customer_fragment_id):
        """Sets the customer_fragment_id of this TargetItemVersion.


        :param customer_fragment_id: The customer_fragment_id of this TargetItemVersion.  # noqa: E501
        :type: str
        """

        self._customer_fragment_id = customer_fragment_id

    @property
    def deletion_date(self):
        """Gets the deletion_date of this TargetItemVersion.  # noqa: E501


        :return: The deletion_date of this TargetItemVersion.  # noqa: E501
        :rtype: datetime
        """
        return self._deletion_date

    @deletion_date.setter
    def deletion_date(self, deletion_date):
        """Sets the deletion_date of this TargetItemVersion.


        :param deletion_date: The deletion_date of this TargetItemVersion.  # noqa: E501
        :type: datetime
        """

        self._deletion_date = deletion_date

    @property
    def item_version_state(self):
        """Gets the item_version_state of this TargetItemVersion.  # noqa: E501

        ItemState defines the different states an Item can be in  # noqa: E501

        :return: The item_version_state of this TargetItemVersion.  # noqa: E501
        :rtype: str
        """
        return self._item_version_state

    @item_version_state.setter
    def item_version_state(self, item_version_state):
        """Sets the item_version_state of this TargetItemVersion.

        ItemState defines the different states an Item can be in  # noqa: E501

        :param item_version_state: The item_version_state of this TargetItemVersion.  # noqa: E501
        :type: str
        """

        self._item_version_state = item_version_state

    @property
    def latest_version(self):
        """Gets the latest_version of this TargetItemVersion.  # noqa: E501


        :return: The latest_version of this TargetItemVersion.  # noqa: E501
        :rtype: bool
        """
        return self._latest_version

    @latest_version.setter
    def latest_version(self, latest_version):
        """Sets the latest_version of this TargetItemVersion.


        :param latest_version: The latest_version of this TargetItemVersion.  # noqa: E501
        :type: bool
        """

        self._latest_version = latest_version

    @property
    def protection_key_name(self):
        """Gets the protection_key_name of this TargetItemVersion.  # noqa: E501


        :return: The protection_key_name of this TargetItemVersion.  # noqa: E501
        :rtype: str
        """
        return self._protection_key_name

    @protection_key_name.setter
    def protection_key_name(self, protection_key_name):
        """Sets the protection_key_name of this TargetItemVersion.


        :param protection_key_name: The protection_key_name of this TargetItemVersion.  # noqa: E501
        :type: str
        """

        self._protection_key_name = protection_key_name

    @property
    def target_name(self):
        """Gets the target_name of this TargetItemVersion.  # noqa: E501


        :return: The target_name of this TargetItemVersion.  # noqa: E501
        :rtype: str
        """
        return self._target_name

    @target_name.setter
    def target_name(self, target_name):
        """Sets the target_name of this TargetItemVersion.


        :param target_name: The target_name of this TargetItemVersion.  # noqa: E501
        :type: str
        """

        self._target_name = target_name

    @property
    def version(self):
        """Gets the version of this TargetItemVersion.  # noqa: E501


        :return: The version of this TargetItemVersion.  # noqa: E501
        :rtype: int
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this TargetItemVersion.


        :param version: The version of this TargetItemVersion.  # noqa: E501
        :type: int
        """

        self._version = version

    @property
    def with_customer_fragment(self):
        """Gets the with_customer_fragment of this TargetItemVersion.  # noqa: E501


        :return: The with_customer_fragment of this TargetItemVersion.  # noqa: E501
        :rtype: bool
        """
        return self._with_customer_fragment

    @with_customer_fragment.setter
    def with_customer_fragment(self, with_customer_fragment):
        """Sets the with_customer_fragment of this TargetItemVersion.


        :param with_customer_fragment: The with_customer_fragment of this TargetItemVersion.  # noqa: E501
        :type: bool
        """

        self._with_customer_fragment = with_customer_fragment

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
        if not isinstance(other, TargetItemVersion):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, TargetItemVersion):
            return True

        return self.to_dict() != other.to_dict()
