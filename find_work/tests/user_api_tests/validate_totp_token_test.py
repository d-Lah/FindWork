import pytest

from django.urls import reverse

from util.error_resp_data import (
    AuthHeadersError,
    FieldsEmptyError,
    WrongTOTPTokenError
)
from util.success_resp_data import ValidateSuccess


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
        assert request.status_code == ValidateSuccess().get_status()
        assert request.data["success"] == (
            ValidateSuccess().get_data()["success"]
        )

    def test_should_response_auth_headers_error(
            self,
            client,
    ):
        request = client.post(
            reverse("user_api:validation_totp_token"),
        )

        assert request.status_code == AuthHeadersError().get_status()
        assert request.data["detail"] == (
            AuthHeadersError().get_data()["detail"]
        )

    def test_should_response_fields_empty_error(
            self,
            client,
            user_auth_headers,
            data_to_validate_totp_token_wo_data
    ):
        request = client.post(
            reverse("user_api:validation_totp_token"),
            headers=user_auth_headers,
            data=data_to_validate_totp_token_wo_data
        )
        assert request.status_code == FieldsEmptyError().get_status()
        assert request.data["fields"] == (
            FieldsEmptyError().get_data()["fields"]
        )

    def test_should_response_wrong_totp_token_error(
            self,
            client,
            user_auth_headers,
            data_to_validate_totp_token_w_wrong_totp_token
    ):
        request = client.post(
            reverse("user_api:validation_totp_token"),
            headers=user_auth_headers,
            data=data_to_validate_totp_token_w_wrong_totp_token
        )
        assert request.status_code == WrongTOTPTokenError().get_status()
        assert request.data["totp_token"] == (
            WrongTOTPTokenError().get_data()["totp_token"]
        )
