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


class UpdateLdapTarget(object):
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
        'bind_dn': 'str',
        'bind_dn_password': 'str',
        'comment': 'str',
        'keep_prev_version': 'str',
        'key': 'str',
        'ldap_ca_cert': 'str',
        'ldap_url': 'str',
        'name': 'str',
        'new_name': 'str',
        'token': 'str',
        'token_expiration': 'str',
        'uid_token': 'str',
        'update_version': 'bool'
    }

    attribute_map = {
        'bind_dn': 'bind-dn',
        'bind_dn_password': 'bind-dn-password',
        'comment': 'comment',
        'keep_prev_version': 'keep-prev-version',
        'key': 'key',
        'ldap_ca_cert': 'ldap-ca-cert',
        'ldap_url': 'ldap-url',
        'name': 'name',
        'new_name': 'new-name',
        'token': 'token',
        'token_expiration': 'token-expiration',
        'uid_token': 'uid-token',
        'update_version': 'update-version'
    }

    def __init__(self, bind_dn=None, bind_dn_password=None, comment=None, keep_prev_version=None, key=None, ldap_ca_cert=None, ldap_url=None, name=None, new_name=None, token=None, token_expiration=None, uid_token=None, update_version=None, local_vars_configuration=None):  # noqa: E501
        """UpdateLdapTarget - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._bind_dn = None
        self._bind_dn_password = None
        self._comment = None
        self._keep_prev_version = None
        self._key = None
        self._ldap_ca_cert = None
        self._ldap_url = None
        self._name = None
        self._new_name = None
        self._token = None
        self._token_expiration = None
        self._uid_token = None
        self._update_version = None
        self.discriminator = None

        if bind_dn is not None:
            self.bind_dn = bind_dn
        if bind_dn_password is not None:
            self.bind_dn_password = bind_dn_password
        if comment is not None:
            self.comment = comment
        if keep_prev_version is not None:
            self.keep_prev_version = keep_prev_version
        if key is not None:
            self.key = key
        if ldap_ca_cert is not None:
            self.ldap_ca_cert = ldap_ca_cert
        if ldap_url is not None:
            self.ldap_url = ldap_url
        self.name = name
        if new_name is not None:
            self.new_name = new_name
        if token is not None:
            self.token = token
        if token_expiration is not None:
            self.token_expiration = token_expiration
        if uid_token is not None:
            self.uid_token = uid_token
        if update_version is not None:
            self.update_version = update_version

    @property
    def bind_dn(self):
        """Gets the bind_dn of this UpdateLdapTarget.  # noqa: E501


        :return: The bind_dn of this UpdateLdapTarget.  # noqa: E501
        :rtype: str
        """
        return self._bind_dn

    @bind_dn.setter
    def bind_dn(self, bind_dn):
        """Sets the bind_dn of this UpdateLdapTarget.


        :param bind_dn: The bind_dn of this UpdateLdapTarget.  # noqa: E501
        :type: str
        """

        self._bind_dn = bind_dn

    @property
    def bind_dn_password(self):
        """Gets the bind_dn_password of this UpdateLdapTarget.  # noqa: E501


        :return: The bind_dn_password of this UpdateLdapTarget.  # noqa: E501
        :rtype: str
        """
        return self._bind_dn_password

    @bind_dn_password.setter
    def bind_dn_password(self, bind_dn_password):
        """Sets the bind_dn_password of this UpdateLdapTarget.


        :param bind_dn_password: The bind_dn_password of this UpdateLdapTarget.  # noqa: E501
        :type: str
        """

        self._bind_dn_password = bind_dn_password

    @property
    def comment(self):
        """Gets the comment of this UpdateLdapTarget.  # noqa: E501

        Comment about the target  # noqa: E501

        :return: The comment of this UpdateLdapTarget.  # noqa: E501
        :rtype: str
        """
        return self._comment

    @comment.setter
    def comment(self, comment):
        """Sets the comment of this UpdateLdapTarget.

        Comment about the target  # noqa: E501

        :param comment: The comment of this UpdateLdapTarget.  # noqa: E501
        :type: str
        """

        self._comment = comment

    @property
    def keep_prev_version(self):
        """Gets the keep_prev_version of this UpdateLdapTarget.  # noqa: E501


        :return: The keep_prev_version of this UpdateLdapTarget.  # noqa: E501
        :rtype: str
        """
        return self._keep_prev_version

    @keep_prev_version.setter
    def keep_prev_version(self, keep_prev_version):
        """Sets the keep_prev_version of this UpdateLdapTarget.


        :param keep_prev_version: The keep_prev_version of this UpdateLdapTarget.  # noqa: E501
        :type: str
        """

        self._keep_prev_version = keep_prev_version

    @property
    def key(self):
        """Gets the key of this UpdateLdapTarget.  # noqa: E501

        The name of a key that used to encrypt the target secret value (if empty, the account default protectionKey key will be used)  # noqa: E501

        :return: The key of this UpdateLdapTarget.  # noqa: E501
        :rtype: str
        """
        return self._key

    @key.setter
    def key(self, key):
        """Sets the key of this UpdateLdapTarget.

        The name of a key that used to encrypt the target secret value (if empty, the account default protectionKey key will be used)  # noqa: E501

        :param key: The key of this UpdateLdapTarget.  # noqa: E501
        :type: str
        """

        self._key = key

    @property
    def ldap_ca_cert(self):
        """Gets the ldap_ca_cert of this UpdateLdapTarget.  # noqa: E501


        :return: The ldap_ca_cert of this UpdateLdapTarget.  # noqa: E501
        :rtype: str
        """
        return self._ldap_ca_cert

    @ldap_ca_cert.setter
    def ldap_ca_cert(self, ldap_ca_cert):
        """Sets the ldap_ca_cert of this UpdateLdapTarget.


        :param ldap_ca_cert: The ldap_ca_cert of this UpdateLdapTarget.  # noqa: E501
        :type: str
        """

        self._ldap_ca_cert = ldap_ca_cert

    @property
    def ldap_url(self):
        """Gets the ldap_url of this UpdateLdapTarget.  # noqa: E501


        :return: The ldap_url of this UpdateLdapTarget.  # noqa: E501
        :rtype: str
        """
        return self._ldap_url

    @ldap_url.setter
    def ldap_url(self, ldap_url):
        """Sets the ldap_url of this UpdateLdapTarget.


        :param ldap_url: The ldap_url of this UpdateLdapTarget.  # noqa: E501
        :type: str
        """

        self._ldap_url = ldap_url

    @property
    def name(self):
        """Gets the name of this UpdateLdapTarget.  # noqa: E501

        Target name  # noqa: E501

        :return: The name of this UpdateLdapTarget.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this UpdateLdapTarget.

        Target name  # noqa: E501

        :param name: The name of this UpdateLdapTarget.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and name is None:  # noqa: E501
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def new_name(self):
        """Gets the new_name of this UpdateLdapTarget.  # noqa: E501

        New target name  # noqa: E501

        :return: The new_name of this UpdateLdapTarget.  # noqa: E501
        :rtype: str
        """
        return self._new_name

    @new_name.setter
    def new_name(self, new_name):
        """Sets the new_name of this UpdateLdapTarget.

        New target name  # noqa: E501

        :param new_name: The new_name of this UpdateLdapTarget.  # noqa: E501
        :type: str
        """

        self._new_name = new_name

    @property
    def token(self):
        """Gets the token of this UpdateLdapTarget.  # noqa: E501

        Authentication token (see `/auth` and `/configure`)  # noqa: E501

        :return: The token of this UpdateLdapTarget.  # noqa: E501
        :rtype: str
        """
        return self._token

    @token.setter
    def token(self, token):
        """Sets the token of this UpdateLdapTarget.

        Authentication token (see `/auth` and `/configure`)  # noqa: E501

        :param token: The token of this UpdateLdapTarget.  # noqa: E501
        :type: str
        """

        self._token = token

    @property
    def token_expiration(self):
        """Gets the token_expiration of this UpdateLdapTarget.  # noqa: E501


        :return: The token_expiration of this UpdateLdapTarget.  # noqa: E501
        :rtype: str
        """
        return self._token_expiration

    @token_expiration.setter
    def token_expiration(self, token_expiration):
        """Sets the token_expiration of this UpdateLdapTarget.


        :param token_expiration: The token_expiration of this UpdateLdapTarget.  # noqa: E501
        :type: str
        """

        self._token_expiration = token_expiration

    @property
    def uid_token(self):
        """Gets the uid_token of this UpdateLdapTarget.  # noqa: E501

        The universal identity token, Required only for universal_identity authentication  # noqa: E501

        :return: The uid_token of this UpdateLdapTarget.  # noqa: E501
        :rtype: str
        """
        return self._uid_token

    @uid_token.setter
    def uid_token(self, uid_token):
        """Sets the uid_token of this UpdateLdapTarget.

        The universal identity token, Required only for universal_identity authentication  # noqa: E501

        :param uid_token: The uid_token of this UpdateLdapTarget.  # noqa: E501
        :type: str
        """

        self._uid_token = uid_token

    @property
    def update_version(self):
        """Gets the update_version of this UpdateLdapTarget.  # noqa: E501

        Deprecated  # noqa: E501

        :return: The update_version of this UpdateLdapTarget.  # noqa: E501
        :rtype: bool
        """
        return self._update_version

    @update_version.setter
    def update_version(self, update_version):
        """Sets the update_version of this UpdateLdapTarget.

        Deprecated  # noqa: E501

        :param update_version: The update_version of this UpdateLdapTarget.  # noqa: E501
        :type: bool
        """

        self._update_version = update_version

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
        if not isinstance(other, UpdateLdapTarget):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, UpdateLdapTarget):
            return True

        return self.to_dict() != other.to_dict()
