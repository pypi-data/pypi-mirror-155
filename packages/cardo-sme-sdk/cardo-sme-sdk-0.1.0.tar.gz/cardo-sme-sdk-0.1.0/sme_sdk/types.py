from typing import TypedDict

BatchResultID = str


class LoginResponseType(TypedDict):
    access_token: str
