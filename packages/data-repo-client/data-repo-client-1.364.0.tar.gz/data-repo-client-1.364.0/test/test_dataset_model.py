# coding: utf-8

"""
    Data Repository API

    <details><summary>This document defines the REST API for the Terra Data Repository.</summary> <p> **Status: design in progress** There are a few top-level endpoints (besides some used by swagger):  * / - generated by swagger: swagger API page that provides this documentation and a live UI for submitting REST requests  * /status - provides the operational status of the service  * /configuration - provides the basic configuration and information about the service  * /api - is the authenticated and authorized Data Repository API  * /ga4gh/drs/v1 - is a transcription of the Data Repository Service API  The API endpoints are organized by interface. Each interface is separately versioned. <p> **Notes on Naming** <p> All of the reference items are suffixed with \\\"Model\\\". Those names are used as the class names in the generated Java code. It is helpful to distinguish these model classes from other related classes, like the DAO classes and the operation classes. </details>   # noqa: E501

    The version of the OpenAPI document: 0.1.0
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import data_repo_client
from data_repo_client.models.dataset_model import DatasetModel  # noqa: E501
from data_repo_client.rest import ApiException

class TestDatasetModel(unittest.TestCase):
    """DatasetModel unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test DatasetModel
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = data_repo_client.models.dataset_model.DatasetModel()  # noqa: E501
        if include_optional :
            return DatasetModel(
                id = '0', 
                name = 'a', 
                description = '0', 
                default_profile_id = '0', 
                data_project = '0', 
                default_snapshot_id = '0', 
                schema = data_repo_client.models.dataset_specification_model.DatasetSpecificationModel(
                    tables = [
                        data_repo_client.models.table_model.TableModel(
                            name = 'a', 
                            columns = [
                                data_repo_client.models.column_model.ColumnModel(
                                    name = 'a', 
                                    datatype = 'string', 
                                    array_of = True, 
                                    required = True, )
                                ], 
                            primary_key = [
                                'a'
                                ], 
                            partition_mode = 'none', 
                            date_partition_options = data_repo_client.models.date_partition_options_model.DatePartitionOptionsModel(
                                column = 'a', ), 
                            int_partition_options = data_repo_client.models.int_partition_options_model.IntPartitionOptionsModel(
                                column = 'a', 
                                min = 56, 
                                max = 56, 
                                interval = 56, ), 
                            row_count = 56, )
                        ], 
                    relationships = [
                        data_repo_client.models.relationship_model.RelationshipModel(
                            name = '0', 
                            from = data_repo_client.models.relationship_term_model.RelationshipTermModel(
                                table = 'a', 
                                column = 'a', ), 
                            to = data_repo_client.models.relationship_term_model.RelationshipTermModel(
                                table = 'a', 
                                column = 'a', ), )
                        ], 
                    assets = [
                        data_repo_client.models.asset_model.AssetModel(
                            name = '0', 
                            tables = [
                                data_repo_client.models.asset_table_model.AssetTableModel(
                                    name = 'a', 
                                    columns = [
                                        'a'
                                        ], )
                                ], 
                            root_table = 'a', 
                            root_column = 'a', 
                            follow = [
                                'a'
                                ], )
                        ], ), 
                created_date = '0', 
                storage = [
                    data_repo_client.models.storage_resource_model.StorageResourceModel(
                        region = '0', 
                        cloud_resource = '0', 
                        cloud_platform = 'gcp', )
                    ], 
                secure_monitoring_enabled = True, 
                phs_id = 'phs123456', 
                access_information = data_repo_client.models.access_info_model.AccessInfoModel(
                    big_query = data_repo_client.models.access_info_big_query_model.AccessInfoBigQueryModel(
                        dataset_name = '0', 
                        dataset_id = '0', 
                        project_id = '0', 
                        link = '0', 
                        tables = [
                            data_repo_client.models.access_info_big_query_model_table.AccessInfoBigQueryModelTable(
                                name = '0', 
                                id = '0', 
                                qualified_name = '0', 
                                link = '0', 
                                sample_query = '0', )
                            ], ), 
                    parquet = data_repo_client.models.access_info_parquet_model.AccessInfoParquetModel(
                        dataset_name = '0', 
                        dataset_id = '0', 
                        storage_account_id = '0', 
                        url = '0', 
                        sas_token = '0', 
                        tables = [
                            data_repo_client.models.access_info_parquet_model_table.AccessInfoParquetModelTable(
                                name = '0', 
                                url = '0', 
                                sas_token = '0', )
                            ], ), ), 
                self_hosted = True, 
                properties = None
            )
        else :
            return DatasetModel(
        )

    def testDatasetModel(self):
        """Test DatasetModel"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
