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
from tiledb.cloud.rest_api.api.array_tasks_api import ArrayTasksApi  # noqa: E501
from tiledb.cloud.rest_api.rest import ApiException


class TestArrayTasksApi(unittest.TestCase):
    """ArrayTasksApi unit test stubs"""

    def setUp(self):
        self.api = (
            tiledb.cloud.rest_api.api.array_tasks_api.ArrayTasksApi()
        )  # noqa: E501

    def tearDown(self):
        pass

    def test_get_array_tasks_sidebar(self):
        """Test case for get_array_tasks_sidebar"""
        pass


if __name__ == "__main__":
    unittest.main()
