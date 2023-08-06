from unittest import mock

import pytest

from sme_sdk import S3BlobStorageClient, UploadFailed, json_to_bytes


def test_boto3_client_is_created_in_init(s3_config):
    s3_client = S3BlobStorageClient(s3_config)

    assert s3_client._client is not None
    assert hasattr(s3_client._client, 'put_object')
    assert hasattr(s3_client._client, 'generate_presigned_url')


@mock.patch('sme_sdk.blob.uuid4')
def test_generate_file_name_will_use_default_if_not_provided(mock_uuid4, s3_client):
    """
    Ensure that default generator is used if not provided.
    """
    mock_uuid4.return_value = '123'

    assert s3_client._generate_file_name({}) == f'companies_{mock_uuid4.return_value}.json'


def test_generate_file_name_will_use_provided_generator(s3_config):
    """
    Ensure that provided generator is used instead of the default one to generate file name.
    """
    file_name = 'file_name.json'
    s3_config.file_name_generator = lambda data: file_name
    s3_client = S3BlobStorageClient(s3_config)

    assert s3_client._generate_file_name({}) == file_name


@mock.patch('sme_sdk.blob.uuid4')
def test_save_data_will_put_data_to_s3(mock_uuid4, s3_client):
    """
    Ensure that data is put to S3 using boto3 client.
    """
    data = {'a': 1, 'b': 2}
    mock_uuid4.return_value = '123'

    with (
        mock.patch.object(s3_client._client, 'put_object') as mock_put_object,
        mock.patch.object(s3_client._client, 'generate_presigned_url') as mock_generate_presigned_url
    ):
        mock_put_object.return_value = {'ResponseMetadata': {'HTTPStatusCode': 200}}
        s3_client.save_data(data)

        mock_put_object.assert_called_once_with(
            Bucket=s3_client.s3_config.bucket_name,
            Key=s3_client._generate_file_name(data),
            Body=json_to_bytes(data)
        )
        mock_generate_presigned_url.assert_called_once_with(
            ClientMethod='get_object',
            Params={
                'Bucket': s3_client.s3_config.bucket_name,
                'Key': s3_client._generate_file_name(data)
            },
            ExpiresIn=s3_client.s3_config.presigned_url_expiration_time
        )


def test_save_data_will_raise_exception_if_upload_failed(s3_client):
    """
    Ensure that UploadFailed exception is raised if upload failed.
    """
    with mock.patch.object(s3_client._client, 'put_object') as mock_put_object:
        mock_put_object.return_value = {'ResponseMetadata': {'HTTPStatusCode': 500}}
        with pytest.raises(UploadFailed):
            s3_client.save_data({})
