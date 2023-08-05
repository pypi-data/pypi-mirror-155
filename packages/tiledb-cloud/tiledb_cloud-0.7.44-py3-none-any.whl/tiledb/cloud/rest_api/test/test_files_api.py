# coding: utf-8

"""
    TileDB Storage Platform API

    TileDB Storage Platform REST API  # noqa: E501

    The version of the OpenAPI document: 2.2.19
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest

import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.api.files_api import FilesApi  # noqa: E501
from tiledb.cloud.rest_api.rest import ApiException


class TestFilesApi(unittest.TestCase):
    """FilesApi unit test stubs"""

    def setUp(self):
        self.api = tiledb.cloud.rest_api.api.files_api.FilesApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_handle_create_file(self):
        """Test case for handle_create_file"""
        pass

    def test_handle_export_file(self):
        """Test case for handle_export_file"""
        pass

    def test_handle_upload_file(self):
        """Test case for handle_upload_file"""
        pass


if __name__ == "__main__":
    unittest.main()
