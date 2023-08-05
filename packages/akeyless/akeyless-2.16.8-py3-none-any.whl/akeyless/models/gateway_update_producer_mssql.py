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


class GatewayUpdateProducerMSSQL(object):
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
        'mssql_create_statements': 'str',
        'mssql_dbname': 'str',
        'mssql_host': 'str',
        'mssql_password': 'str',
        'mssql_port': 'str',
        'mssql_revocation_statements': 'str',
        'mssql_username': 'str',
        'name': 'str',
        'new_name': 'str',
        'producer_encryption_key_name': 'str',
        'secure_access_bastion_issuer': 'str',
        'secure_access_db_schema': 'str',
        'secure_access_enable': 'str',
        'secure_access_host': 'list[str]',
        'secure_access_web': 'bool',
        'tags': 'list[str]',
        'target_name': 'str',
        'token': 'str',
        'uid_token': 'str',
        'user_ttl': 'str'
    }

    attribute_map = {
        'mssql_create_statements': 'mssql-create-statements',
        'mssql_dbname': 'mssql-dbname',
        'mssql_host': 'mssql-host',
        'mssql_password': 'mssql-password',
        'mssql_port': 'mssql-port',
        'mssql_revocation_statements': 'mssql-revocation-statements',
        'mssql_username': 'mssql-username',
        'name': 'name',
        'new_name': 'new-name',
        'producer_encryption_key_name': 'producer-encryption-key-name',
        'secure_access_bastion_issuer': 'secure-access-bastion-issuer',
        'secure_access_db_schema': 'secure-access-db-schema',
        'secure_access_enable': 'secure-access-enable',
        'secure_access_host': 'secure-access-host',
        'secure_access_web': 'secure-access-web',
        'tags': 'tags',
        'target_name': 'target-name',
        'token': 'token',
        'uid_token': 'uid-token',
        'user_ttl': 'user-ttl'
    }

    def __init__(self, mssql_create_statements=None, mssql_dbname=None, mssql_host='127.0.0.1', mssql_password=None, mssql_port='1433', mssql_revocation_statements=None, mssql_username=None, name=None, new_name=None, producer_encryption_key_name=None, secure_access_bastion_issuer=None, secure_access_db_schema=None, secure_access_enable=None, secure_access_host=None, secure_access_web=None, tags=None, target_name=None, token=None, uid_token=None, user_ttl='60m', local_vars_configuration=None):  # noqa: E501
        """GatewayUpdateProducerMSSQL - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._mssql_create_statements = None
        self._mssql_dbname = None
        self._mssql_host = None
        self._mssql_password = None
        self._mssql_port = None
        self._mssql_revocation_statements = None
        self._mssql_username = None
        self._name = None
        self._new_name = None
        self._producer_encryption_key_name = None
        self._secure_access_bastion_issuer = None
        self._secure_access_db_schema = None
        self._secure_access_enable = None
        self._secure_access_host = None
        self._secure_access_web = None
        self._tags = None
        self._target_name = None
        self._token = None
        self._uid_token = None
        self._user_ttl = None
        self.discriminator = None

        if mssql_create_statements is not None:
            self.mssql_create_statements = mssql_create_statements
        if mssql_dbname is not None:
            self.mssql_dbname = mssql_dbname
        if mssql_host is not None:
            self.mssql_host = mssql_host
        if mssql_password is not None:
            self.mssql_password = mssql_password
        if mssql_port is not None:
            self.mssql_port = mssql_port
        if mssql_revocation_statements is not None:
            self.mssql_revocation_statements = mssql_revocation_statements
        if mssql_username is not None:
            self.mssql_username = mssql_username
        self.name = name
        if new_name is not None:
            self.new_name = new_name
        if producer_encryption_key_name is not None:
            self.producer_encryption_key_name = producer_encryption_key_name
        if secure_access_bastion_issuer is not None:
            self.secure_access_bastion_issuer = secure_access_bastion_issuer
        if secure_access_db_schema is not None:
            self.secure_access_db_schema = secure_access_db_schema
        if secure_access_enable is not None:
            self.secure_access_enable = secure_access_enable
        if secure_access_host is not None:
            self.secure_access_host = secure_access_host
        if secure_access_web is not None:
            self.secure_access_web = secure_access_web
        if tags is not None:
            self.tags = tags
        if target_name is not None:
            self.target_name = target_name
        if token is not None:
            self.token = token
        if uid_token is not None:
            self.uid_token = uid_token
        if user_ttl is not None:
            self.user_ttl = user_ttl

    @property
    def mssql_create_statements(self):
        """Gets the mssql_create_statements of this GatewayUpdateProducerMSSQL.  # noqa: E501

        MSSQL Creation statements  # noqa: E501

        :return: The mssql_create_statements of this GatewayUpdateProducerMSSQL.  # noqa: E501
        :rtype: str
        """
        return self._mssql_create_statements

    @mssql_create_statements.setter
    def mssql_create_statements(self, mssql_create_statements):
        """Sets the mssql_create_statements of this GatewayUpdateProducerMSSQL.

        MSSQL Creation statements  # noqa: E501

        :param mssql_create_statements: The mssql_create_statements of this GatewayUpdateProducerMSSQL.  # noqa: E501
        :type: str
        """

        self._mssql_create_statements = mssql_create_statements

    @property
    def mssql_dbname(self):
        """Gets the mssql_dbname of this GatewayUpdateProducerMSSQL.  # noqa: E501

        MSSQL Name  # noqa: E501

        :return: The mssql_dbname of this GatewayUpdateProducerMSSQL.  # noqa: E501
        :rtype: str
        """
        return self._mssql_dbname

    @mssql_dbname.setter
    def mssql_dbname(self, mssql_dbname):
        """Sets the mssql_dbname of this GatewayUpdateProducerMSSQL.

        MSSQL Name  # noqa: E501

        :param mssql_dbname: The mssql_dbname of this GatewayUpdateProducerMSSQL.  # noqa: E501
        :type: str
        """

        self._mssql_dbname = mssql_dbname

    @property
    def mssql_host(self):
        """Gets the mssql_host of this GatewayUpdateProducerMSSQL.  # noqa: E501

        MSSQL Host  # noqa: E501

        :return: The mssql_host of this GatewayUpdateProducerMSSQL.  # noqa: E501
        :rtype: str
        """
        return self._mssql_host

    @mssql_host.setter
    def mssql_host(self, mssql_host):
        """Sets the mssql_host of this GatewayUpdateProducerMSSQL.

        MSSQL Host  # noqa: E501

        :param mssql_host: The mssql_host of this GatewayUpdateProducerMSSQL.  # noqa: E501
        :type: str
        """

        self._mssql_host = mssql_host

    @property
    def mssql_password(self):
        """Gets the mssql_password of this GatewayUpdateProducerMSSQL.  # noqa: E501

        MSSQL Password  # noqa: E501

        :return: The mssql_password of this GatewayUpdateProducerMSSQL.  # noqa: E501
        :rtype: str
        """
        return self._mssql_password

    @mssql_password.setter
    def mssql_password(self, mssql_password):
        """Sets the mssql_password of this GatewayUpdateProducerMSSQL.

        MSSQL Password  # noqa: E501

        :param mssql_password: The mssql_password of this GatewayUpdateProducerMSSQL.  # noqa: E501
        :type: str
        """

        self._mssql_password = mssql_password

    @property
    def mssql_port(self):
        """Gets the mssql_port of this GatewayUpdateProducerMSSQL.  # noqa: E501

        MSSQL Port  # noqa: E501

        :return: The mssql_port of this GatewayUpdateProducerMSSQL.  # noqa: E501
        :rtype: str
        """
        return self._mssql_port

    @mssql_port.setter
    def mssql_port(self, mssql_port):
        """Sets the mssql_port of this GatewayUpdateProducerMSSQL.

        MSSQL Port  # noqa: E501

        :param mssql_port: The mssql_port of this GatewayUpdateProducerMSSQL.  # noqa: E501
        :type: str
        """

        self._mssql_port = mssql_port

    @property
    def mssql_revocation_statements(self):
        """Gets the mssql_revocation_statements of this GatewayUpdateProducerMSSQL.  # noqa: E501

        MSSQL Revocation statements  # noqa: E501

        :return: The mssql_revocation_statements of this GatewayUpdateProducerMSSQL.  # noqa: E501
        :rtype: str
        """
        return self._mssql_revocation_statements

    @mssql_revocation_statements.setter
    def mssql_revocation_statements(self, mssql_revocation_statements):
        """Sets the mssql_revocation_statements of this GatewayUpdateProducerMSSQL.

        MSSQL Revocation statements  # noqa: E501

        :param mssql_revocation_statements: The mssql_revocation_statements of this GatewayUpdateProducerMSSQL.  # noqa: E501
        :type: str
        """

        self._mssql_revocation_statements = mssql_revocation_statements

    @property
    def mssql_username(self):
        """Gets the mssql_username of this GatewayUpdateProducerMSSQL.  # noqa: E501

        MSSQL Username  # noqa: E501

        :return: The mssql_username of this GatewayUpdateProducerMSSQL.  # noqa: E501
        :rtype: str
        """
        return self._mssql_username

    @mssql_username.setter
    def mssql_username(self, mssql_username):
        """Sets the mssql_username of this GatewayUpdateProducerMSSQL.

        MSSQL Username  # noqa: E501

        :param mssql_username: The mssql_username of this GatewayUpdateProducerMSSQL.  # noqa: E501
        :type: str
        """

        self._mssql_username = mssql_username

    @property
    def name(self):
        """Gets the name of this GatewayUpdateProducerMSSQL.  # noqa: E501

        Producer name  # noqa: E501

        :return: The name of this GatewayUpdateProducerMSSQL.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this GatewayUpdateProducerMSSQL.

        Producer name  # noqa: E501

        :param name: The name of this GatewayUpdateProducerMSSQL.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and name is None:  # noqa: E501
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def new_name(self):
        """Gets the new_name of this GatewayUpdateProducerMSSQL.  # noqa: E501

        Producer name  # noqa: E501

        :return: The new_name of this GatewayUpdateProducerMSSQL.  # noqa: E501
        :rtype: str
        """
        return self._new_name

    @new_name.setter
    def new_name(self, new_name):
        """Sets the new_name of this GatewayUpdateProducerMSSQL.

        Producer name  # noqa: E501

        :param new_name: The new_name of this GatewayUpdateProducerMSSQL.  # noqa: E501
        :type: str
        """

        self._new_name = new_name

    @property
    def producer_encryption_key_name(self):
        """Gets the producer_encryption_key_name of this GatewayUpdateProducerMSSQL.  # noqa: E501

        Dynamic producer encryption key  # noqa: E501

        :return: The producer_encryption_key_name of this GatewayUpdateProducerMSSQL.  # noqa: E501
        :rtype: str
        """
        return self._producer_encryption_key_name

    @producer_encryption_key_name.setter
    def producer_encryption_key_name(self, producer_encryption_key_name):
        """Sets the producer_encryption_key_name of this GatewayUpdateProducerMSSQL.

        Dynamic producer encryption key  # noqa: E501

        :param producer_encryption_key_name: The producer_encryption_key_name of this GatewayUpdateProducerMSSQL.  # noqa: E501
        :type: str
        """

        self._producer_encryption_key_name = producer_encryption_key_name

    @property
    def secure_access_bastion_issuer(self):
        """Gets the secure_access_bastion_issuer of this GatewayUpdateProducerMSSQL.  # noqa: E501


        :return: The secure_access_bastion_issuer of this GatewayUpdateProducerMSSQL.  # noqa: E501
        :rtype: str
        """
        return self._secure_access_bastion_issuer

    @secure_access_bastion_issuer.setter
    def secure_access_bastion_issuer(self, secure_access_bastion_issuer):
        """Sets the secure_access_bastion_issuer of this GatewayUpdateProducerMSSQL.


        :param secure_access_bastion_issuer: The secure_access_bastion_issuer of this GatewayUpdateProducerMSSQL.  # noqa: E501
        :type: str
        """

        self._secure_access_bastion_issuer = secure_access_bastion_issuer

    @property
    def secure_access_db_schema(self):
        """Gets the secure_access_db_schema of this GatewayUpdateProducerMSSQL.  # noqa: E501


        :return: The secure_access_db_schema of this GatewayUpdateProducerMSSQL.  # noqa: E501
        :rtype: str
        """
        return self._secure_access_db_schema

    @secure_access_db_schema.setter
    def secure_access_db_schema(self, secure_access_db_schema):
        """Sets the secure_access_db_schema of this GatewayUpdateProducerMSSQL.


        :param secure_access_db_schema: The secure_access_db_schema of this GatewayUpdateProducerMSSQL.  # noqa: E501
        :type: str
        """

        self._secure_access_db_schema = secure_access_db_schema

    @property
    def secure_access_enable(self):
        """Gets the secure_access_enable of this GatewayUpdateProducerMSSQL.  # noqa: E501


        :return: The secure_access_enable of this GatewayUpdateProducerMSSQL.  # noqa: E501
        :rtype: str
        """
        return self._secure_access_enable

    @secure_access_enable.setter
    def secure_access_enable(self, secure_access_enable):
        """Sets the secure_access_enable of this GatewayUpdateProducerMSSQL.


        :param secure_access_enable: The secure_access_enable of this GatewayUpdateProducerMSSQL.  # noqa: E501
        :type: str
        """

        self._secure_access_enable = secure_access_enable

    @property
    def secure_access_host(self):
        """Gets the secure_access_host of this GatewayUpdateProducerMSSQL.  # noqa: E501


        :return: The secure_access_host of this GatewayUpdateProducerMSSQL.  # noqa: E501
        :rtype: list[str]
        """
        return self._secure_access_host

    @secure_access_host.setter
    def secure_access_host(self, secure_access_host):
        """Sets the secure_access_host of this GatewayUpdateProducerMSSQL.


        :param secure_access_host: The secure_access_host of this GatewayUpdateProducerMSSQL.  # noqa: E501
        :type: list[str]
        """

        self._secure_access_host = secure_access_host

    @property
    def secure_access_web(self):
        """Gets the secure_access_web of this GatewayUpdateProducerMSSQL.  # noqa: E501


        :return: The secure_access_web of this GatewayUpdateProducerMSSQL.  # noqa: E501
        :rtype: bool
        """
        return self._secure_access_web

    @secure_access_web.setter
    def secure_access_web(self, secure_access_web):
        """Sets the secure_access_web of this GatewayUpdateProducerMSSQL.


        :param secure_access_web: The secure_access_web of this GatewayUpdateProducerMSSQL.  # noqa: E501
        :type: bool
        """

        self._secure_access_web = secure_access_web

    @property
    def tags(self):
        """Gets the tags of this GatewayUpdateProducerMSSQL.  # noqa: E501

        List of the tags attached to this secret  # noqa: E501

        :return: The tags of this GatewayUpdateProducerMSSQL.  # noqa: E501
        :rtype: list[str]
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """Sets the tags of this GatewayUpdateProducerMSSQL.

        List of the tags attached to this secret  # noqa: E501

        :param tags: The tags of this GatewayUpdateProducerMSSQL.  # noqa: E501
        :type: list[str]
        """

        self._tags = tags

    @property
    def target_name(self):
        """Gets the target_name of this GatewayUpdateProducerMSSQL.  # noqa: E501

        Target name  # noqa: E501

        :return: The target_name of this GatewayUpdateProducerMSSQL.  # noqa: E501
        :rtype: str
        """
        return self._target_name

    @target_name.setter
    def target_name(self, target_name):
        """Sets the target_name of this GatewayUpdateProducerMSSQL.

        Target name  # noqa: E501

        :param target_name: The target_name of this GatewayUpdateProducerMSSQL.  # noqa: E501
        :type: str
        """

        self._target_name = target_name

    @property
    def token(self):
        """Gets the token of this GatewayUpdateProducerMSSQL.  # noqa: E501

        Authentication token (see `/auth` and `/configure`)  # noqa: E501

        :return: The token of this GatewayUpdateProducerMSSQL.  # noqa: E501
        :rtype: str
        """
        return self._token

    @token.setter
    def token(self, token):
        """Sets the token of this GatewayUpdateProducerMSSQL.

        Authentication token (see `/auth` and `/configure`)  # noqa: E501

        :param token: The token of this GatewayUpdateProducerMSSQL.  # noqa: E501
        :type: str
        """

        self._token = token

    @property
    def uid_token(self):
        """Gets the uid_token of this GatewayUpdateProducerMSSQL.  # noqa: E501

        The universal identity token, Required only for universal_identity authentication  # noqa: E501

        :return: The uid_token of this GatewayUpdateProducerMSSQL.  # noqa: E501
        :rtype: str
        """
        return self._uid_token

    @uid_token.setter
    def uid_token(self, uid_token):
        """Sets the uid_token of this GatewayUpdateProducerMSSQL.

        The universal identity token, Required only for universal_identity authentication  # noqa: E501

        :param uid_token: The uid_token of this GatewayUpdateProducerMSSQL.  # noqa: E501
        :type: str
        """

        self._uid_token = uid_token

    @property
    def user_ttl(self):
        """Gets the user_ttl of this GatewayUpdateProducerMSSQL.  # noqa: E501

        User TTL  # noqa: E501

        :return: The user_ttl of this GatewayUpdateProducerMSSQL.  # noqa: E501
        :rtype: str
        """
        return self._user_ttl

    @user_ttl.setter
    def user_ttl(self, user_ttl):
        """Sets the user_ttl of this GatewayUpdateProducerMSSQL.

        User TTL  # noqa: E501

        :param user_ttl: The user_ttl of this GatewayUpdateProducerMSSQL.  # noqa: E501
        :type: str
        """

        self._user_ttl = user_ttl

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
        if not isinstance(other, GatewayUpdateProducerMSSQL):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, GatewayUpdateProducerMSSQL):
            return True

        return self.to_dict() != other.to_dict()
