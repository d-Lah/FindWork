from rest_framework.exceptions import APIException
from rest_framework import status


class NotFoundException(APIException):
    status_code = status.HTTP_404_NOT_FOUND

    def __init__(self, detail):
        self.detail = {"detail": detail}


class InvalidFileExtException(APIException):
    status_code = status.HTTP_415_UNSUPPORTED_MEDIA_TYPE

    def __init__(self, detail):
        self.detail = {"detail": detail}


class FileSizeTooLargeException(APIException):
    status_code = status.HTTP_413_REQUEST_ENTITY_TOO_LARGE

    def __init__(self, detail):
        self.detail = {"detail": detail}


class TOTPIncapException(APIException):
    status_code = status.HTTP_403_FORBIDDEN

    def __init__(self, detail):
        self.detail = {"detail": detail}


class AlreadyEnableOrDisableException(APIException):
    status_code = status.HTTP_409_CONFLICT

    def __init__(self, detail):
        self.detail = {"detail": detail}


class UserActivationUUIDIncapException(APIException):
    status_code = status.HTTP_409_CONFLICT

    def __init__(self, detail):
        self.detail = {"detail": detail}


class WrongPasswordException(APIException):
    status_code = status.HTTP_403_FORBIDDEN

    def __init__(self, detail):
        self.detail = {"detail": detail}
