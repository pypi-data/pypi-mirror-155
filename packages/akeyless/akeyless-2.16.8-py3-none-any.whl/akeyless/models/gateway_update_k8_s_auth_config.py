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


class GatewayUpdateK8SAuthConfig(object):
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
        'access_id': 'str',
        'config_encryption_key_name': 'str',
        'k8s_ca_cert': 'str',
        'k8s_host': 'str',
        'k8s_issuer': 'str',
        'name': 'str',
        'new_name': 'str',
        'signing_key': 'str',
        'token': 'str',
        'token_exp': 'int',
        'token_reviewer_jwt': 'str',
        'uid_token': 'str'
    }

    attribute_map = {
        'access_id': 'access-id',
        'config_encryption_key_name': 'config-encryption-key-name',
        'k8s_ca_cert': 'k8s-ca-cert',
        'k8s_host': 'k8s-host',
        'k8s_issuer': 'k8s-issuer',
        'name': 'name',
        'new_name': 'new-name',
        'signing_key': 'signing-key',
        'token': 'token',
        'token_exp': 'token-exp',
        'token_reviewer_jwt': 'token-reviewer-jwt',
        'uid_token': 'uid-token'
    }

    def __init__(self, access_id=None, config_encryption_key_name=None, k8s_ca_cert=None, k8s_host=None, k8s_issuer=None, name=None, new_name=None, signing_key=None, token=None, token_exp=None, token_reviewer_jwt=None, uid_token=None, local_vars_configuration=None):  # noqa: E501
        """GatewayUpdateK8SAuthConfig - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._access_id = None
        self._config_encryption_key_name = None
        self._k8s_ca_cert = None
        self._k8s_host = None
        self._k8s_issuer = None
        self._name = None
        self._new_name = None
        self._signing_key = None
        self._token = None
        self._token_exp = None
        self._token_reviewer_jwt = None
        self._uid_token = None
        self.discriminator = None

        self.access_id = access_id
        if config_encryption_key_name is not None:
            self.config_encryption_key_name = config_encryption_key_name
        if k8s_ca_cert is not None:
            self.k8s_ca_cert = k8s_ca_cert
        self.k8s_host = k8s_host
        if k8s_issuer is not None:
            self.k8s_issuer = k8s_issuer
        self.name = name
        self.new_name = new_name
        self.signing_key = signing_key
        if token is not None:
            self.token = token
        if token_exp is not None:
            self.token_exp = token_exp
        if token_reviewer_jwt is not None:
            self.token_reviewer_jwt = token_reviewer_jwt
        if uid_token is not None:
            self.uid_token = uid_token

    @property
    def access_id(self):
        """Gets the access_id of this GatewayUpdateK8SAuthConfig.  # noqa: E501

        The access ID of the Kubernetes auth method  # noqa: E501

        :return: The access_id of this GatewayUpdateK8SAuthConfig.  # noqa: E501
        :rtype: str
        """
        return self._access_id

    @access_id.setter
    def access_id(self, access_id):
        """Sets the access_id of this GatewayUpdateK8SAuthConfig.

        The access ID of the Kubernetes auth method  # noqa: E501

        :param access_id: The access_id of this GatewayUpdateK8SAuthConfig.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and access_id is None:  # noqa: E501
            raise ValueError("Invalid value for `access_id`, must not be `None`")  # noqa: E501

        self._access_id = access_id

    @property
    def config_encryption_key_name(self):
        """Gets the config_encryption_key_name of this GatewayUpdateK8SAuthConfig.  # noqa: E501

        Config encryption key  # noqa: E501

        :return: The config_encryption_key_name of this GatewayUpdateK8SAuthConfig.  # noqa: E501
        :rtype: str
        """
        return self._config_encryption_key_name

    @config_encryption_key_name.setter
    def config_encryption_key_name(self, config_encryption_key_name):
        """Sets the config_encryption_key_name of this GatewayUpdateK8SAuthConfig.

        Config encryption key  # noqa: E501

        :param config_encryption_key_name: The config_encryption_key_name of this GatewayUpdateK8SAuthConfig.  # noqa: E501
        :type: str
        """

        self._config_encryption_key_name = config_encryption_key_name

    @property
    def k8s_ca_cert(self):
        """Gets the k8s_ca_cert of this GatewayUpdateK8SAuthConfig.  # noqa: E501

        The CA Cert (in PEM format) to use to call into the kubernetes API server  # noqa: E501

        :return: The k8s_ca_cert of this GatewayUpdateK8SAuthConfig.  # noqa: E501
        :rtype: str
        """
        return self._k8s_ca_cert

    @k8s_ca_cert.setter
    def k8s_ca_cert(self, k8s_ca_cert):
        """Sets the k8s_ca_cert of this GatewayUpdateK8SAuthConfig.

        The CA Cert (in PEM format) to use to call into the kubernetes API server  # noqa: E501

        :param k8s_ca_cert: The k8s_ca_cert of this GatewayUpdateK8SAuthConfig.  # noqa: E501
        :type: str
        """

        self._k8s_ca_cert = k8s_ca_cert

    @property
    def k8s_host(self):
        """Gets the k8s_host of this GatewayUpdateK8SAuthConfig.  # noqa: E501

        The URL of the kubernetes API server  # noqa: E501

        :return: The k8s_host of this GatewayUpdateK8SAuthConfig.  # noqa: E501
        :rtype: str
        """
        return self._k8s_host

    @k8s_host.setter
    def k8s_host(self, k8s_host):
        """Sets the k8s_host of this GatewayUpdateK8SAuthConfig.

        The URL of the kubernetes API server  # noqa: E501

        :param k8s_host: The k8s_host of this GatewayUpdateK8SAuthConfig.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and k8s_host is None:  # noqa: E501
            raise ValueError("Invalid value for `k8s_host`, must not be `None`")  # noqa: E501

        self._k8s_host = k8s_host

    @property
    def k8s_issuer(self):
        """Gets the k8s_issuer of this GatewayUpdateK8SAuthConfig.  # noqa: E501

        The Kubernetes JWT issuer name. If not set, kubernetes/serviceaccount will use as an issuer.  # noqa: E501

        :return: The k8s_issuer of this GatewayUpdateK8SAuthConfig.  # noqa: E501
        :rtype: str
        """
        return self._k8s_issuer

    @k8s_issuer.setter
    def k8s_issuer(self, k8s_issuer):
        """Sets the k8s_issuer of this GatewayUpdateK8SAuthConfig.

        The Kubernetes JWT issuer name. If not set, kubernetes/serviceaccount will use as an issuer.  # noqa: E501

        :param k8s_issuer: The k8s_issuer of this GatewayUpdateK8SAuthConfig.  # noqa: E501
        :type: str
        """

        self._k8s_issuer = k8s_issuer

    @property
    def name(self):
        """Gets the name of this GatewayUpdateK8SAuthConfig.  # noqa: E501

        K8S Auth config name  # noqa: E501

        :return: The name of this GatewayUpdateK8SAuthConfig.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this GatewayUpdateK8SAuthConfig.

        K8S Auth config name  # noqa: E501

        :param name: The name of this GatewayUpdateK8SAuthConfig.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and name is None:  # noqa: E501
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def new_name(self):
        """Gets the new_name of this GatewayUpdateK8SAuthConfig.  # noqa: E501

        K8S Auth config new name  # noqa: E501

        :return: The new_name of this GatewayUpdateK8SAuthConfig.  # noqa: E501
        :rtype: str
        """
        return self._new_name

    @new_name.setter
    def new_name(self, new_name):
        """Sets the new_name of this GatewayUpdateK8SAuthConfig.

        K8S Auth config new name  # noqa: E501

        :param new_name: The new_name of this GatewayUpdateK8SAuthConfig.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and new_name is None:  # noqa: E501
            raise ValueError("Invalid value for `new_name`, must not be `None`")  # noqa: E501

        self._new_name = new_name

    @property
    def signing_key(self):
        """Gets the signing_key of this GatewayUpdateK8SAuthConfig.  # noqa: E501

        The private key (in base64 encoded of the PEM format) associated with the public key defined in the Kubernetes auth  # noqa: E501

        :return: The signing_key of this GatewayUpdateK8SAuthConfig.  # noqa: E501
        :rtype: str
        """
        return self._signing_key

    @signing_key.setter
    def signing_key(self, signing_key):
        """Sets the signing_key of this GatewayUpdateK8SAuthConfig.

        The private key (in base64 encoded of the PEM format) associated with the public key defined in the Kubernetes auth  # noqa: E501

        :param signing_key: The signing_key of this GatewayUpdateK8SAuthConfig.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and signing_key is None:  # noqa: E501
            raise ValueError("Invalid value for `signing_key`, must not be `None`")  # noqa: E501

        self._signing_key = signing_key

    @property
    def token(self):
        """Gets the token of this GatewayUpdateK8SAuthConfig.  # noqa: E501

        Authentication token (see `/auth` and `/configure`)  # noqa: E501

        :return: The token of this GatewayUpdateK8SAuthConfig.  # noqa: E501
        :rtype: str
        """
        return self._token

    @token.setter
    def token(self, token):
        """Sets the token of this GatewayUpdateK8SAuthConfig.

        Authentication token (see `/auth` and `/configure`)  # noqa: E501

        :param token: The token of this GatewayUpdateK8SAuthConfig.  # noqa: E501
        :type: str
        """

        self._token = token

    @property
    def token_exp(self):
        """Gets the token_exp of this GatewayUpdateK8SAuthConfig.  # noqa: E501

        Time in seconds of expiration of the Akeyless Kube Auth Method token  # noqa: E501

        :return: The token_exp of this GatewayUpdateK8SAuthConfig.  # noqa: E501
        :rtype: int
        """
        return self._token_exp

    @token_exp.setter
    def token_exp(self, token_exp):
        """Sets the token_exp of this GatewayUpdateK8SAuthConfig.

        Time in seconds of expiration of the Akeyless Kube Auth Method token  # noqa: E501

        :param token_exp: The token_exp of this GatewayUpdateK8SAuthConfig.  # noqa: E501
        :type: int
        """

        self._token_exp = token_exp

    @property
    def token_reviewer_jwt(self):
        """Gets the token_reviewer_jwt of this GatewayUpdateK8SAuthConfig.  # noqa: E501

        A Kubernetes service account JWT used to access the TokenReview API to validate other JWTs. If not set, the JWT submitted in the authentication process will be used to access the Kubernetes TokenReview API.  # noqa: E501

        :return: The token_reviewer_jwt of this GatewayUpdateK8SAuthConfig.  # noqa: E501
        :rtype: str
        """
        return self._token_reviewer_jwt

    @token_reviewer_jwt.setter
    def token_reviewer_jwt(self, token_reviewer_jwt):
        """Sets the token_reviewer_jwt of this GatewayUpdateK8SAuthConfig.

        A Kubernetes service account JWT used to access the TokenReview API to validate other JWTs. If not set, the JWT submitted in the authentication process will be used to access the Kubernetes TokenReview API.  # noqa: E501

        :param token_reviewer_jwt: The token_reviewer_jwt of this GatewayUpdateK8SAuthConfig.  # noqa: E501
        :type: str
        """

        self._token_reviewer_jwt = token_reviewer_jwt

    @property
    def uid_token(self):
        """Gets the uid_token of this GatewayUpdateK8SAuthConfig.  # noqa: E501

        The universal identity token, Required only for universal_identity authentication  # noqa: E501

        :return: The uid_token of this GatewayUpdateK8SAuthConfig.  # noqa: E501
        :rtype: str
        """
        return self._uid_token

    @uid_token.setter
    def uid_token(self, uid_token):
        """Sets the uid_token of this GatewayUpdateK8SAuthConfig.

        The universal identity token, Required only for universal_identity authentication  # noqa: E501

        :param uid_token: The uid_token of this GatewayUpdateK8SAuthConfig.  # noqa: E501
        :type: str
        """

        self._uid_token = uid_token

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
        if not isinstance(other, GatewayUpdateK8SAuthConfig):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, GatewayUpdateK8SAuthConfig):
            return True

        return self.to_dict() != other.to_dict()
