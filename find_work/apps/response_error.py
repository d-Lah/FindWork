from abc import (
    ABC,
    abstractmethod
)
from rest_framework import status
from rest_framework.response import Response


class ResponseError(ABC):
    @classmethod
    @abstractmethod
    def get_response(self):
        pass

    @classmethod
    @abstractmethod
    def add_data_for_response_data(self, key, value):
        pass


class ResponseEmailAlreadyExistsError(ResponseError):
    response_data = {
        "error": "EmailAlreadyExistsError"
    }

    def get_response(self):
        return Response(
            self.response_data,
            status=status.HTTP_409_CONFLICT
        )

    def add_data_for_response_data(self, key, value):
        pass


class ResponsePhoneNumberAlreadyExistsError(ResponseError):
    response_data = {
        "error": "PhoneNumberAlreadyExistsError"
    }

    def get_response(self):
        return Response(
            self.response_data,
            status=status.HTTP_409_CONFLICT
        )

    def add_data_for_response_data(self, key, value):
        pass


class ResponseUserFieldEmptyError(ResponseError):
    response_data = {
        "error": "UserFieldEmptyError"
    }

    def get_response(self):
        return Response(
            self.response_data,
            status=status.HTTP_400_BAD_REQUEST
        )

    def add_data_for_response_data(self, key, value):
        pass


class ResponseProfileFieldEmptyError(ResponseError):
    response_data = {
        "error": "ProfileFieldEmptyError"
    }

    def get_response(self):
        return Response(
            self.response_data,
            status=status.HTTP_400_BAD_REQUEST
        )

    def add_data_for_response_data(self, key, value):
        pass


class ResponseUserAlreadyActiveError(ResponseError):
    response_data = {
        "error": "UserAlreadyActiveError"
    }

    def get_response(self):
        return Response(
            self.response_data,
            status=status.HTTP_409_CONFLICT
        )

    def add_data_for_response_data(self, key, value):
        pass


class ResponseTOTPTokenFieldEmptyError(ResponseError):
    response_data = {
        "error": "TOTPTokenFieldEmptyError"
    }

    def get_response(self):
        return Response(
            self.response_data,
            status=status.HTTP_400_BAD_REQUEST
        )

    def add_data_for_response_data(self, key, value):
        pass


class ResponseTwoFactorAuthAlreadyActiveError(ResponseError):
    response_data = {
        "error": "TwoFactorAlreadyActiveError"
    }

    def get_response(self):
        return Response(
            self.response_data,
            status=status.HTTP_409_CONFLICT
        )

    def add_data_for_response_data(self, key, value):
        pass


class ResponseWrongTOTPTokenError(ResponseError):
    response_data = {
        "error": "WrongTOTPTokenError"
    }

    def get_response(self):
        return Response(
            self.response_data,
            status=status.HTTP_401_UNAUTHORIZED
        )

    def add_data_for_response_data(self, key, value):
        pass


class ResponsePasswordFieldEmptyError(ResponseError):
    response_data = {
        "error": "PasswordFieldEmptyError"
    }

    def get_response(self):
        return Response(
            self.response_data,
            status=status.HTTP_400_BAD_REQUEST
        )

    def add_data_for_response_data(self, key, value):
        pass


class ResponseWrongPasswordError(ResponseError):
    response_data = {
        "error": "WrongPasswordError"
    }

    def get_response(self):
        return Response(
            self.response_data,
            status=status.HTTP_401_UNAUTHORIZED
        )

    def add_data_for_response_data(self, key, value):
        pass


class ResponseEmailFieldEmptyError(ResponseError):
    response_data = {
        "error": "EmailFieldEmpty"
    }

    def get_response(self):
        return Response(
            self.response_data,
            status=status.HTTP_400_BAD_REQUEST
        )

    def add_data_for_response_data(self, key, value):
        pass


class ResponsePhoneNumberFieldEmptyError(ResponseError):
    response_data = {
        "error": "PhoneNumberFieldEmpty"
    }

    def get_response(self):
        return Response(
            self.response_data,
            status=status.HTTP_400_BAD_REQUEST
        )

    def add_data_for_response_data(self, key, value):
        pass
