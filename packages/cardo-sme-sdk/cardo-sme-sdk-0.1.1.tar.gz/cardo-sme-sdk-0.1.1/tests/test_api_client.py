from unittest import mock
from unittest.mock import MagicMock

import pytest

from sme_sdk import APIClient, BatchCreationFailed, BatchResultRetrieveFailed, LoginFailed


def test_form_url_prefix_urls_with_host(api_client):
    """
    Ensure that the form_url method prefixes the url with the host and takes
    care of the leading and trailing slashes.
    """
    assert api_client._form_url('/api/v1/login') == 'http://localhost:8080/api/v1/login'


@mock.patch('sme_sdk.api.APIClient.login')
def test_entering_performs_login(login_mock: MagicMock, api_config):
    """
    Ensure that entering the context performs a login.
    """
    with APIClient(api_config):
        login_mock.assert_called_once()


@mock.patch('sme_sdk.api.requests.post')
def test_when_login_successful_access_token_is_set(post_mock: MagicMock, api_client):
    """
    Ensure that when the login is successful the access token is set.
    """
    post_mock.return_value.status_code = 200
    post_mock.return_value.json.return_value = {'access_token': 'access_token'}
    with api_client:
        assert api_client._access_token == 'access_token'


@mock.patch('sme_sdk.api.requests.post')
def test_when_login_fails_exception_is_raised(post_mock: MagicMock, api_client, failed_response):
    """
    Ensure that when the login fails an exception is raised.
    """
    post_mock.return_value = failed_response
    with pytest.raises(LoginFailed):
        api_client.login()


@mock.patch('sme_sdk.api.requests.post')
def test_create_new_batch_return_response_data_at_success(
    mock_post: MagicMock,
    mock_blob_storage,
    success_response,
    api_client,
):
    """
    Ensure that the create_new_batch method accepts any blob storage.
    The only condition is that the blob storage has to implement BlobStorageClient abs class.
    """
    mock_post.return_value = success_response
    response = api_client.create_new_batch(data=None, blob_storage_client=mock_blob_storage)

    mock_post.assert_called_once()
    assert response == success_response.json()


@mock.patch('sme_sdk.api.requests.post')
def test_create_new_batch_raise_error_at_failure(
    mock_post: MagicMock,
    mock_blob_storage,
    failed_response,
    api_client,
):
    """
    Ensure that the create_new_batch method accepts any blob storage.
    The only condition is that the blob storage has to implement BlobStorageClient abs class.
    """
    mock_post.return_value = failed_response

    with pytest.raises(BatchCreationFailed):
        api_client.create_new_batch(data=None, blob_storage_client=mock_blob_storage)


@mock.patch('sme_sdk.api.requests.get')
def test_get_batch_result_return_response_data_at_success(
    mock_get: MagicMock,
    success_response,
    api_client,
):
    """
    Ensure that the get_batch_result method returns the response data.
    """
    mock_get.return_value = success_response
    response = api_client.get_batch_result(batch_id='123')

    mock_get.assert_called_once()
    assert response == mock_get.return_value.json()


@mock.patch('sme_sdk.api.requests.get')
def test_get_batch_result_raise_error_at_failure(
    mock_get: MagicMock,
    failed_response,
    api_client,
):
    """
    Ensure that the get_batch_result method raises an error.
    """
    mock_get.return_value = failed_response

    with pytest.raises(BatchResultRetrieveFailed):
        api_client.get_batch_result(batch_id='123')
