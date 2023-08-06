class APIException(Exception):
    """
    Base class for all API exceptions.
    """

    def __init__(self, message, status_code):
        super().__init__(message, status_code)


class LoginFailed(APIException):
    pass


class BatchCreationFailed(APIException):
    pass


class BatchResultRetrieveFailed(APIException):
    pass


class UploadFailed(APIException):
    pass
