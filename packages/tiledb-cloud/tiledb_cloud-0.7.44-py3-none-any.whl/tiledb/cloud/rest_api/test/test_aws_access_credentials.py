# coding: utf-8

"""
    TileDB Storage Platform API

    TileDB Storage Platform REST API  # noqa: E501

    The version of the OpenAPI document: 2.2.19
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import datetime
import unittest

import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.models.aws_access_credentials import (  # noqa: E501
    AWSAccessCredentials,
)
from tiledb.cloud.rest_api.rest import ApiException


class TestAWSAccessCredentials(unittest.TestCase):
    """AWSAccessCredentials unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test AWSAccessCredentials
        include_option is a boolean, when False only required
        params are included, when True both required and
        optional params are included"""
        # model = tiledb.cloud.rest_api.models.aws_access_credentials.AWSAccessCredentials()  # noqa: E501
        if include_optional:
            return AWSAccessCredentials(
                secret_access_key="0",
                access_key_id="0",
                service_role_arn="0",
                name="0",
                default=True,
                buckets=["s3://company-bucket-1/tiledb/"],
                created_at=datetime.datetime.strptime(
                    "2013-10-20 19:20:30.00", "%Y-%m-%d %H:%M:%S.%f"
                ),
                updated_at=datetime.datetime.strptime(
                    "2013-10-20 19:20:30.00", "%Y-%m-%d %H:%M:%S.%f"
                ),
            )
        else:
            return AWSAccessCredentials()

    def testAWSAccessCredentials(self):
        """Test AWSAccessCredentials"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == "__main__":
    unittest.main()
