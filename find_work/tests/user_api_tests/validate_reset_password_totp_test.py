import pytest

from django.urls import reverse

from util.error_resp_data import (
    FieldsEmptyError,
    UserNotFoundError,
    InvalidEmailAdressError,
    ResetPasswordTOTPIncapError
)
from util.success_resp_data import ValidateSuccess


@pytest.mark.django_db
class TestValidateResetPassword:
    def test_should_validate_reset_password_totp(
            self,
            client,
            data_to_validate_reset_password_totp
    ):
        request = client.post(
            reverse("user_api:validate_reset_password_totp"),
            data=data_to_validate_reset_password_totp
        )
        assert request.status_code == ValidateSuccess().get_status()
        assert request.data["success"] == (
            ValidateSuccess().get_data()["success"]
        )

    def test_should_response_fields_empty_error(
            self,
            client,
            data_to_validate_reset_password_totp_wo_data,
    ):
        request = client.post(
            reverse("user_api:validate_reset_password_totp"),
            data=data_to_validate_reset_password_totp_wo_data
        )
        assert request.status_code == FieldsEmptyError().get_status()
        assert request.data["fields"] == (
            FieldsEmptyError().get_data()["fields"]
        )

    def test_should_response_invalid_email_error(
            self,
            client,
            data_to_validate_reset_password_totp_w_invalid_email
    ):
        request = client.post(
            reverse("user_api:validate_reset_password_totp"),
            data=data_to_validate_reset_password_totp_w_invalid_email
        )
        assert request.status_code == InvalidEmailAdressError().get_status()
        assert request.data["email"] == (
            InvalidEmailAdressError().get_data()["email"]
        )

    def test_should_response_user_not_found_error(
            self,
            client,
            data_to_validate_reset_password_totp_w_wrong_email
    ):
        request = client.post(
            reverse("user_api:validate_reset_password_totp"),
            data=data_to_validate_reset_password_totp_w_wrong_email
        )
        assert request.status_code == UserNotFoundError().get_status()
        assert request.data["user"] == (
            UserNotFoundError().get_data()["user"]
        )

    def test_should_response_reset_password_totp_incapacitated(
            self,
            client,
            data_to_validate_reset_password_totp_w_incap_reset_password_totp
    ):
        data = (
            data_to_validate_reset_password_totp_w_incap_reset_password_totp
        )
        request = client.post(
            reverse("user_api:validate_reset_password_totp"),
            data=data
        )
        assert request.status_code == (
            ResetPasswordTOTPIncapError().get_status()
        )
        assert request.data["reset_password_totp"] == (
            ResetPasswordTOTPIncapError().get_data()["reset_password_totp"]
        )
