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
from tiledb.cloud.rest_api.models.generic_udf import GenericUDF  # noqa: E501
from tiledb.cloud.rest_api.rest import ApiException


class TestGenericUDF(unittest.TestCase):
    """GenericUDF unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test GenericUDF
        include_option is a boolean, when False only required
        params are included, when True both required and
        optional params are included"""
        # model = tiledb.cloud.rest_api.models.generic_udf.GenericUDF()  # noqa: E501
        if include_optional:
            return GenericUDF(
                udf_info_name="TileDB-Inc/csv_ingestor",
                language="python",
                version="0",
                image_name="0",
                resource_class="standard",
                _exec="0",
                exec_raw="0",
                argument="0",
                stored_param_uuids=["229f38c4-ba89-43d6-ab88-bae3bcca7969"],
                result_format="python_pickle",
                task_name="0",
                store_results=True,
                timeout=56,
                dont_download_results=True,
                task_graph_uuid="0",
                client_node_uuid="0",
            )
        else:
            return GenericUDF()

    def testGenericUDF(self):
        """Test GenericUDF"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == "__main__":
    unittest.main()
