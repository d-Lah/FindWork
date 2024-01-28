import pytest

from django.urls import reverse

from util.error_resp_data import (
    FieldsEmptyError,
    UserNotFoundError,
    InvalidEmailAdressError,
)
from util.success_resp_data import CreateSuccess


@pytest.mark.django_db
class TestGenerateResetPasswordTOTP:
    def test_should_generate_reset_password_totp(
            self,
            client,
            mocker,
            data_to_generate_reset_password_totp
    ):
        mocker.patch(
            "util.mail_sender.send_mail",
            return_value=True
        )

        request = client.post(
            reverse("user_api:generate_reset_password_totp"),
            data=data_to_generate_reset_password_totp
        )
        assert request.status_code == CreateSuccess().get_status()
        assert request.data["success"] == (
            CreateSuccess().get_data()["success"]
        )

    def test_should_response_fields_empty_error(
            self,
            client,
            data_to_generate_reset_password_totp_wo_email
    ):
        request = client.post(
            reverse("user_api:generate_reset_password_totp"),
            data=data_to_generate_reset_password_totp_wo_email
        )
        assert request.status_code == FieldsEmptyError().get_status()
        assert request.data["fields"] == (
            FieldsEmptyError().get_data()["fields"]
        )

    def test_should_response_invalid_email_error(
            self,
            client,
            data_to_generate_reset_password_totp_w_invalid_email
    ):
        request = client.post(
            reverse("user_api:generate_reset_password_totp"),
            data=data_to_generate_reset_password_totp_w_invalid_email
        )
        assert request.status_code == InvalidEmailAdressError().get_status()
        assert request.data["email"] == (
            InvalidEmailAdressError().get_data()["email"]
        )

    def test_should_response_user_not_found_error(
            self,
            client,
            data_to_generate_reset_password_totp_w_wrong_email,
    ):
        request = client.post(
            reverse("user_api:generate_reset_password_totp"),
            data=data_to_generate_reset_password_totp_w_wrong_email
        )
        assert request.status_code == UserNotFoundError().get_status()
        assert request.data["user"] == (
            UserNotFoundError().get_data()["user"]
        )
