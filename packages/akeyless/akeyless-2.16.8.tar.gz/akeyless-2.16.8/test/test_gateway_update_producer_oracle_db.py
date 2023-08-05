# coding: utf-8

"""
    Akeyless API

    The purpose of this application is to provide access to Akeyless API.  # noqa: E501

    The version of the OpenAPI document: 2.0
    Contact: support@akeyless.io
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import akeyless
from akeyless.models.gateway_update_producer_oracle_db import GatewayUpdateProducerOracleDb  # noqa: E501
from akeyless.rest import ApiException

class TestGatewayUpdateProducerOracleDb(unittest.TestCase):
    """GatewayUpdateProducerOracleDb unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test GatewayUpdateProducerOracleDb
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = akeyless.models.gateway_update_producer_oracle_db.GatewayUpdateProducerOracleDb()  # noqa: E501
        if include_optional :
            return GatewayUpdateProducerOracleDb(
                db_server_certificates = '0', 
                db_server_name = '0', 
                name = '0', 
                new_name = '0', 
                oracle_host = '127.0.0.1', 
                oracle_password = '0', 
                oracle_port = '1521', 
                oracle_screation_statements = '0', 
                oracle_service_name = '0', 
                oracle_username = '0', 
                password = '0', 
                producer_encryption_key_name = '0', 
                tags = [
                    '0'
                    ], 
                target_name = '0', 
                token = '0', 
                uid_token = '0', 
                user_ttl = '60m', 
                username = '0'
            )
        else :
            return GatewayUpdateProducerOracleDb(
                name = '0',
        )

    def testGatewayUpdateProducerOracleDb(self):
        """Test GatewayUpdateProducerOracleDb"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
