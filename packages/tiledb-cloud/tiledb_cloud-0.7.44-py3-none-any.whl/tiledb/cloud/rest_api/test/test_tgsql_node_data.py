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
from tiledb.cloud.rest_api.models.tgsql_node_data import TGSQLNodeData  # noqa: E501
from tiledb.cloud.rest_api.rest import ApiException


class TestTGSQLNodeData(unittest.TestCase):
    """TGSQLNodeData unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test TGSQLNodeData
        include_option is a boolean, when False only required
        params are included, when True both required and
        optional params are included"""
        # model = tiledb.cloud.rest_api.models.tgsql_node_data.TGSQLNodeData()  # noqa: E501
        if include_optional:
            return TGSQLNodeData(
                init_commands=["0"],
                query="0",
                parameters=[tiledb.cloud.rest_api.models.tg_arg_value.TGArgValue()],
                result_format="python_pickle",
            )
        else:
            return TGSQLNodeData()

    def testTGSQLNodeData(self):
        """Test TGSQLNodeData"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == "__main__":
    unittest.main()
