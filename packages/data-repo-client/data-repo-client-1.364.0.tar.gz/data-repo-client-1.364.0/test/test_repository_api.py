# coding: utf-8

"""
    Data Repository API

    <details><summary>This document defines the REST API for the Terra Data Repository.</summary> <p> **Status: design in progress** There are a few top-level endpoints (besides some used by swagger):  * / - generated by swagger: swagger API page that provides this documentation and a live UI for submitting REST requests  * /status - provides the operational status of the service  * /configuration - provides the basic configuration and information about the service  * /api - is the authenticated and authorized Data Repository API  * /ga4gh/drs/v1 - is a transcription of the Data Repository Service API  The API endpoints are organized by interface. Each interface is separately versioned. <p> **Notes on Naming** <p> All of the reference items are suffixed with \\\"Model\\\". Those names are used as the class names in the generated Java code. It is helpful to distinguish these model classes from other related classes, like the DAO classes and the operation classes. </details>   # noqa: E501

    The version of the OpenAPI document: 0.1.0
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest

import data_repo_client
from data_repo_client.api.repository_api import RepositoryApi  # noqa: E501
from data_repo_client.rest import ApiException


class TestRepositoryApi(unittest.TestCase):
    """RepositoryApi unit test stubs"""

    def setUp(self):
        self.api = data_repo_client.api.repository_api.RepositoryApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_add_dataset_asset_specifications(self):
        """Test case for add_dataset_asset_specifications

        """
        pass

    def test_add_dataset_policy_member(self):
        """Test case for add_dataset_policy_member

        """
        pass

    def test_add_snapshot_policy_member(self):
        """Test case for add_snapshot_policy_member

        """
        pass

    def test_apply_dataset_data_deletion(self):
        """Test case for apply_dataset_data_deletion

        """
        pass

    def test_bulk_file_load(self):
        """Test case for bulk_file_load

        """
        pass

    def test_bulk_file_load_array(self):
        """Test case for bulk_file_load_array

        """
        pass

    def test_bulk_file_results_delete(self):
        """Test case for bulk_file_results_delete

        """
        pass

    def test_close_transaction(self):
        """Test case for close_transaction

        """
        pass

    def test_create_dataset(self):
        """Test case for create_dataset

        """
        pass

    def test_create_search_index(self):
        """Test case for create_search_index

        """
        pass

    def test_create_snapshot(self):
        """Test case for create_snapshot

        """
        pass

    def test_delete_dataset(self):
        """Test case for delete_dataset

        """
        pass

    def test_delete_dataset_policy_member(self):
        """Test case for delete_dataset_policy_member

        """
        pass

    def test_delete_file(self):
        """Test case for delete_file

        """
        pass

    def test_delete_snapshot(self):
        """Test case for delete_snapshot

        """
        pass

    def test_delete_snapshot_policy_member(self):
        """Test case for delete_snapshot_policy_member

        """
        pass

    def test_enumerate_datasets(self):
        """Test case for enumerate_datasets

        """
        pass

    def test_enumerate_jobs(self):
        """Test case for enumerate_jobs

        """
        pass

    def test_enumerate_snapshots(self):
        """Test case for enumerate_snapshots

        """
        pass

    def test_enumerate_transactions(self):
        """Test case for enumerate_transactions

        """
        pass

    def test_export_snapshot(self):
        """Test case for export_snapshot

        """
        pass

    def test_get_config(self):
        """Test case for get_config

        """
        pass

    def test_get_config_list(self):
        """Test case for get_config_list

        """
        pass

    def test_get_load_history_for_load_tag(self):
        """Test case for get_load_history_for_load_tag

        """
        pass

    def test_ingest_dataset(self):
        """Test case for ingest_dataset

        """
        pass

    def test_ingest_file(self):
        """Test case for ingest_file

        """
        pass

    def test_lookup_file_by_id(self):
        """Test case for lookup_file_by_id

        """
        pass

    def test_lookup_file_by_path(self):
        """Test case for lookup_file_by_path

        """
        pass

    def test_lookup_snapshot_file_by_id(self):
        """Test case for lookup_snapshot_file_by_id

        """
        pass

    def test_lookup_snapshot_file_by_path(self):
        """Test case for lookup_snapshot_file_by_path

        """
        pass

    def test_lookup_snapshot_preview_by_id(self):
        """Test case for lookup_snapshot_preview_by_id

        """
        pass

    def test_open_transaction(self):
        """Test case for open_transaction

        """
        pass

    def test_patch_dataset(self):
        """Test case for patch_dataset

        """
        pass

    def test_patch_snapshot(self):
        """Test case for patch_snapshot

        """
        pass

    def test_query_search_indices(self):
        """Test case for query_search_indices

        """
        pass

    def test_remove_dataset_asset_specifications(self):
        """Test case for remove_dataset_asset_specifications

        """
        pass

    def test_reset_config(self):
        """Test case for reset_config

        """
        pass

    def test_retrieve_dataset(self):
        """Test case for retrieve_dataset

        """
        pass

    def test_retrieve_dataset_policies(self):
        """Test case for retrieve_dataset_policies

        """
        pass

    def test_retrieve_job(self):
        """Test case for retrieve_job

        """
        pass

    def test_retrieve_job_result(self):
        """Test case for retrieve_job_result

        """
        pass

    def test_retrieve_snapshot(self):
        """Test case for retrieve_snapshot

        """
        pass

    def test_retrieve_snapshot_policies(self):
        """Test case for retrieve_snapshot_policies

        """
        pass

    def test_retrieve_transaction(self):
        """Test case for retrieve_transaction

        """
        pass

    def test_retrieve_user_dataset_roles(self):
        """Test case for retrieve_user_dataset_roles

        """
        pass

    def test_retrieve_user_snapshot_roles(self):
        """Test case for retrieve_user_snapshot_roles

        """
        pass

    def test_set_config_list(self):
        """Test case for set_config_list

        """
        pass

    def test_set_fault(self):
        """Test case for set_fault

        """
        pass

    def test_update_schema(self):
        """Test case for update_schema

        """
        pass

    def test_upgrade(self):
        """Test case for upgrade

        """
        pass

    def test_user(self):
        """Test case for user

        """
        pass


if __name__ == '__main__':
    unittest.main()
