from dataclasses import dataclass
from typing import Callable, Optional


@dataclass
class APIConfig:
    host: str
    username: str
    password: str


@dataclass
class S3Config:
    access_key_id: str
    secret_access_key: str
    bucket_name: str
    region_name: str
    presigned_url_expiration_time: int = 3600
    file_name_generator: Optional[Callable] = None
