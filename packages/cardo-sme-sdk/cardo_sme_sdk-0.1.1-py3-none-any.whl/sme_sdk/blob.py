from abc import ABC, abstractmethod
from uuid import uuid4

import boto3

from sme_sdk.config import S3Config
from sme_sdk.exceptions import UploadFailed
from sme_sdk.utils import json_to_bytes


class BlobStorageClient(ABC):

    @abstractmethod
    def save_data(self, data) -> str:
        raise NotImplementedError()


class S3BlobStorageClient(BlobStorageClient):
    SERVICE_NAME = 's3'

    def __init__(self, s3_config: S3Config):
        self.s3_config = s3_config
        self._client = self._create_client()

    def _create_client(self):
        return boto3.client(
            self.SERVICE_NAME,
            aws_access_key_id=self.s3_config.access_key_id,
            aws_secret_access_key=self.s3_config.secret_access_key,
            region_name=self.s3_config.region_name
        )

    @staticmethod
    def _default_file_name_generator(data) -> str:
        return f'companies_{uuid4()}.json'

    def _generate_file_name(self, data) -> str:
        generator = self.s3_config.file_name_generator or self._default_file_name_generator
        return generator(data)

    def _create_presigned_url(self, file_name) -> str:
        return self._client.generate_presigned_url(
            ClientMethod='get_object',
            Params={
                'Bucket': self.s3_config.bucket_name,
                'Key': file_name
            },
            ExpiresIn=self.s3_config.presigned_url_expiration_time
        )

    def save_data(self, data) -> str:
        file_name = self._generate_file_name(data)
        response = self._client.put_object(
            Bucket=self.s3_config.bucket_name,
            Key=file_name,
            Body=json_to_bytes(data)
        )
        if (status_code := response['ResponseMetadata']['HTTPStatusCode']) != 200:
            raise UploadFailed('S3 upload failed', status_code)

        return self._create_presigned_url(file_name)
