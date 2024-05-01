import pytest

from django.urls import reverse

from rest_framework import status

from util import error_resp_data
from util import success_resp_data


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

        assert request.status_code == success_resp_data.validate["status_code"]
        assert request.data["detail"] == (
            success_resp_data.validate["data"]["detail"]
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

        assert request.status_code == status.HTTP_400_BAD_REQUEST
        for field in request.data:
            assert request.data[field][0] == error_resp_data.field_is_blank

    def test_should_response_invalid_email_error(
            self,
            client,
            data_to_validate_reset_password_totp_w_invalid_email
    ):
        request = client.post(
            reverse("user_api:validate_reset_password_totp"),
            data=data_to_validate_reset_password_totp_w_invalid_email
        )

        assert request.status_code == status.HTTP_400_BAD_REQUEST
        assert request.data["email"][0] == error_resp_data.invalid_email

    def test_should_response_user_not_found_error(
            self,
            client,
            data_to_validate_reset_password_totp_w_wrong_email
    ):
        request = client.post(
            reverse("user_api:validate_reset_password_totp"),
            data=data_to_validate_reset_password_totp_w_wrong_email
        )

        assert request.status_code == status.HTTP_404_NOT_FOUND
        assert request.data["detail"] == (
            error_resp_data.user_with_given_email_not_found
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

        assert request.status_code == status.HTTP_403_FORBIDDEN
        assert request.data["detail"] == (
            error_resp_data.reset_password_totp_incap
        )
