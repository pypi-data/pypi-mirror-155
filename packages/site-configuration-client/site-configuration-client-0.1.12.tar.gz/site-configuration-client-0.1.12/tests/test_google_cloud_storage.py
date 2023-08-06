"""
Tests for GoogleCloudStorage
"""
import logging

from unittest.mock import patch, Mock
from google.api_core.exceptions import NotFound

from site_config_client.google_cloud_storage import GoogleCloudStorage


def get_mock_gcp_client(mock_blob):
    mock_bucket = Mock()
    mock_bucket.get_blob.return_value = mock_blob

    mock_client = Mock()
    mock_client.get_bucket.return_value = mock_bucket
    return mock_client


@patch('google.cloud.storage.Client')
def test_gcp_storage(client_cls):
    mock_blob = Mock()
    mock_blob.download_as_bytes.return_value = b'{"name": "my_site"}'
    client_cls.return_value = get_mock_gcp_client(mock_blob)
    storage = GoogleCloudStorage('random_bucket_name')

    content = storage.read('some_file.json')

    assert content == '{"name": "my_site"}'


@patch('google.cloud.storage.Client')
def test_gcp_storage_not_found(client_cls, caplog):
    caplog.set_level(logging.INFO)
    mock_blob = Mock()
    mock_blob.download_as_bytes.side_effect = NotFound('file not found')
    client_cls.return_value = get_mock_gcp_client(mock_blob)
    storage = GoogleCloudStorage('random_bucket_name')

    content = storage.read('some_file.json')

    assert content is None, \
        'If the file not found, the siteconfg.Client should take of this case'
    assert 'File path not found: some_file.json' in caplog.text


@patch('google.cloud.storage.Client')
def test_gcp_storage_blob_is_none(client_cls, caplog):
    """
    Google Cloud Storage returns a `None` blob, ensure this case is handled.
    """
    caplog.set_level(logging.INFO)
    client_cls.return_value = get_mock_gcp_client(mock_blob=None)
    storage = GoogleCloudStorage('random_bucket_name')

    content = storage.read('some_file.json')

    assert content is None, \
        'If the file not found, the siteconfg.Client should take of this case'
    assert 'File path not found: some_file.json' in caplog.text
