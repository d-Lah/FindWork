import pytest

from django.urls import reverse

from rest_framework import status

from util.user_api_resp.validate_reset_password_totp_resp import (
    ValidateResetPasswordTOTPResp
)


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
        assert request.status_code == status.HTTP_200_OK
        assert request.data["success"] == (
            ValidateResetPasswordTOTPResp.resp_data["successes"][0]["success"]
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
        assert request.data["error"] == (
            ValidateResetPasswordTOTPResp.resp_data["errors"][0]["error"]
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
        assert request.status_code == status.HTTP_404_NOT_FOUND
        assert request.data["error"] == (
            ValidateResetPasswordTOTPResp.resp_data["errors"][2]["error"]
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
        assert request.data["error"] == (
            ValidateResetPasswordTOTPResp.resp_data["errors"][3]["error"]
        )
