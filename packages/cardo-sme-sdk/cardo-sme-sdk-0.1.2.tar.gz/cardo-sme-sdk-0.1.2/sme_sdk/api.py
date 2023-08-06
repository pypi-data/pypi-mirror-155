from contextlib import ContextDecorator
from functools import cached_property
from typing import Literal
from urllib import parse

import requests

from sme_sdk.config import APIConfig
from sme_sdk.blob import BlobStorageClient
from sme_sdk.exceptions import BatchCreationFailed, BatchResultRetrieveFailed, LoginFailed
from sme_sdk.types import BatchResultID, LoginResponseType
from sme_sdk.urls import Url


class APIClient(ContextDecorator):
    ACCESS_TOKEN_NAME: Literal['access_token'] = 'access_token'
    FILE_URL_NAME = 'file_url'

    def __init__(self, api_config: APIConfig):
        self.api_config = api_config
        self._access_token = None

    def __enter__(self):
        login_response = self.login()
        self._access_token = login_response[self.ACCESS_TOKEN_NAME]

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def _form_url(self, partial_url) -> str:
        return parse.urljoin(self.api_config.host, partial_url)

    @cached_property
    def _login_data(self):
        return {
            'username': self.api_config.username,
            'password': self.api_config.password,
        }

    @cached_property
    def _headers(self):
        return {
            'Authorization': f'Bearer {self._access_token}',
        }

    def login(self) -> LoginResponseType:
        url = self._form_url(Url.login.value)
        response = requests.post(url, json=self._login_data)
        if response.status_code == 200:
            return response.json()
        else:
            raise LoginFailed(message=response.text, status_code=response.status_code)

    def create_new_batch(self, data, blob_storage_client: BlobStorageClient) -> BatchResultID:
        file_url = blob_storage_client.save_data(data)
        response = requests.post(
            url=self._form_url(Url.new_batch.value),
            json={self.FILE_URL_NAME: file_url},
            headers=self._headers
        )
        if response.status_code == 200:
            return response.json()
        else:
            raise BatchCreationFailed(response.text, response.status_code)

    def get_batch_result(self, batch_id: BatchResultID):
        response = requests.get(
            url=f'{self._form_url(Url.batch_result.value)}/{batch_id}',
            headers=self._headers
        )
        if response.status_code == 200:
            return response.json()
        else:
            raise BatchResultRetrieveFailed(response.text, response.status_code)
