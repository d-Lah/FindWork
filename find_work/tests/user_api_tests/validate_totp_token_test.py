import pytest

from django.urls import reverse

from rest_framework import status

from apps.response_error import (
    ResponseWrongTOTPTokenError,
    ResponseTOTPTokenFieldEmptyError,
)
from apps.response_success import (
    ResponseValid,
)


@pytest.mark.django_db
class TestValidateTOTPToken:
    def test_should_validate_totp_token(
            self,
            client,
            user_auth_headers,
            data_to_validate_totp_token
    ):
        request = client.post(
            reverse("user_api:validation_totp_token"),
            headers=user_auth_headers,
            data=data_to_validate_totp_token
        )
        assert request.status_code == status.HTTP_200_OK
        assert request.data.get(
            "status") == ResponseValid.response_data["status"]

    def test_should_response_auth_headers_error(
            self,
            client,
    ):
        request = client.post(
            reverse("user_api:validation_totp_token"),
        )
        assert request.status_code == status.HTTP_401_UNAUTHORIZED

    def test_should_response_totp_token_field_empty_error(
            self,
            client,
            user_auth_headers
    ):
        request = client.post(
            reverse("user_api:validation_totp_token"),
            headers=user_auth_headers,
        )
        assert request.status_code == status.HTTP_400_BAD_REQUEST
        assert request.data.get("error") == (
            ResponseTOTPTokenFieldEmptyError.response_data["error"]
        )

    def test_should_response_wrong_totp_token_error(
            self,
            client,
            user_auth_headers,
            validate_totp_token_data_to_response_wrong_totp_token_error
    ):
        request = client.post(
            reverse("user_api:validation_totp_token"),
            headers=user_auth_headers,
            data=validate_totp_token_data_to_response_wrong_totp_token_error
        )
        assert request.status_code == status.HTTP_401_UNAUTHORIZED
        assert request.data.get("error") == (
            ResponseWrongTOTPTokenError.response_data["error"]
        )
