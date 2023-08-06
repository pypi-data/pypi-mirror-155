import pytest

from sme_sdk import APIClient, APIConfig, BlobStorageClient, S3BlobStorageClient, S3Config


class MockResponse:
    def __init__(self, status_code, json_data):
        self.status_code = status_code
        self.json_data = json_data
        self.text = 'Mock text'

    def json(self):
        return self.json_data


@pytest.fixture
def api_config():
    return APIConfig(
        host='http://localhost:8080',
        username='username',
        password='password',
    )


@pytest.fixture
def s3_config():
    return S3Config(
        access_key_id='access_key_id',
        secret_access_key='secret_access_key',
        region_name='region-name',
        bucket_name='bucket_name'
    )


@pytest.fixture
def api_client(api_config):
    return APIClient(api_config)


@pytest.fixture
def s3_client(s3_config):
    return S3BlobStorageClient(s3_config)


@pytest.fixture
def mock_blob_storage():
    class MockBlobStorage(BlobStorageClient):
        def save_data(self, data):
            return 'http://localhost:8080/api/v1/blob/123'

    return MockBlobStorage()


@pytest.fixture
def success_response():
    return MockResponse(200, {"data": "success"})


@pytest.fixture
def failed_response():
    return MockResponse(400, {"data": "failed"})
