import pytest

from django.urls import reverse

from rest_framework import status

from apps.response_error import (
    ResponseUserNotFoundError,
    ResponseEmailFieldEmptyError,
    ResponseTOTPTokenFieldEmptyError,
    ResponseResetPasswordTOTPIncapacitatedError,
)
from apps.response_success import ResponseValid


@pytest.mark.django_db
class TestValidateUserResetPassword:
    def test_should_validate_user_reset_password_totp(
            self,
            client,
            data_to_validate_user_reset_password_totp
    ):
        request = client.post(
            reverse("user_api:validate_user_reset_password_totp"),
            data=data_to_validate_user_reset_password_totp
        )
        assert request.status_code == status.HTTP_200_OK
        assert request.data.get("status") == (
            ResponseValid.response_data["status"]
        )

    def test_should_response_email_field_empty_error(
            self,
            client,
            validate_user_reset_password_totp_data_to_response_email_field_empty_error,
    ):
        request = client.post(
            reverse("user_api:validate_user_reset_password_totp"),
            data=validate_user_reset_password_totp_data_to_response_email_field_empty_error
        )
        assert request.status_code == status.HTTP_400_BAD_REQUEST
        assert request.data.get("error") == (
            ResponseEmailFieldEmptyError.response_data["error"]
        )

    def test_should_response_reset_password_totp_field_empty_error(
            self,
            client,
            data_to_response_reset_password_totp_field_empty_error
    ):
        request = client.post(
            reverse("user_api:validate_user_reset_password_totp"),
            data=data_to_response_reset_password_totp_field_empty_error
        )
        assert request.status_code == status.HTTP_400_BAD_REQUEST
        assert request.data.get("error") == (
            ResponseTOTPTokenFieldEmptyError.response_data["error"]
        )

    def test_should_response_user_not_found_error(
            self,
            client,
            validate_user_reset_password_totp_data_to_response_user_not_found_error
    ):
        request = client.post(
            reverse("user_api:validate_user_reset_password_totp"),
            data=validate_user_reset_password_totp_data_to_response_user_not_found_error
        )
        assert request.status_code == status.HTTP_404_NOT_FOUND
        assert request.data.get("error") == (
            ResponseUserNotFoundError.response_data["error"]
        )

    def test_should_response_reset_password_totp_incapacitated(
            self,
            client,
            response_reset_password_totp_incapacitated_error
    ):
        request = client.post(
            reverse("user_api:validate_user_reset_password_totp"),
            data=response_reset_password_totp_incapacitated_error
        )
        assert request.status_code == status.HTTP_403_FORBIDDEN
        assert request.data.get("error") == (
            ResponseResetPasswordTOTPIncapacitatedError.response_data["error"]
        )
