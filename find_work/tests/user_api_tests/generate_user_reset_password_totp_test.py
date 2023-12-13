import pytest

from django.urls import reverse

from rest_framework import status

from apps.response_error import (
    ResponseUserNotFoundError,
    ResponseEmailFieldEmptyError,
)
from apps.response_success import ResponseCreate


@pytest.mark.django_db
class TestGenerateUserResetPasswordTOTP:
    def test_should_generate_user_reset_password_totp(
            self,
            client,
            mocker,
            data_for_test_should_generate_user_reset_password_totp
    ):
        mocker.patch(
            "apps.mail_sender.send_mail",
            return_value=True
        )

        request = client.post(
            reverse("user_api:generate_user_reset_password_totp"),
            data=data_for_test_should_generate_user_reset_password_totp
        )
        assert request.status_code == status.HTTP_201_CREATED
        assert request.data.get("status") == (
            ResponseCreate.response_data["status"]
        )

    def generate_user_reset_password_totp_test_should_response_email_field_empty_error(
            self,
            client,
    ):
        request = client.post(
            reverse("user_api:generate_user_reset_password_totp"),
        )
        assert request.status_code == status.HTTP_400_BAD_REQUEST
        assert request.data.get("error") == (
            ResponseEmailFieldEmptyError.response_data["error"]
        )

    def generate_user_reset_password_totp_test_should_response_user_not_found_error(
            self,
            client,
            generate_user_reset_password_totp_data_for_response_user_not_found_error,
    ):
        data = (
            generate_user_reset_password_totp_data_for_response_user_not_found_error
        )
        request = client.post(
            reverse("user_api:generate_user_reset_password_totp"),
            data=data
        )
        assert request.status_code == status.HTTP_404_NOT_FOUND
        assert request.data.get("error") == (
            ResponseUserNotFoundError.response_data["error"]
        )
