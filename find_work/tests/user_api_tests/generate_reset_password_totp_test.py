import pytest

from django.urls import reverse

from rest_framework import status

from util.user_api_resp.generate_reset_password_totp_resp import (
    GenerateResetPasswordTOTPResp
)


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
        assert request.status_code == status.HTTP_201_CREATED
        assert request.data["success"] == (
            GenerateResetPasswordTOTPResp.resp_data["successes"][0]["success"]
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
        assert request.status_code == status.HTTP_400_BAD_REQUEST
        assert request.data["error"] == (
            GenerateResetPasswordTOTPResp.resp_data["errors"][0]["error"]
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
        assert request.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert request.data["error"] == (
            GenerateResetPasswordTOTPResp.resp_data["errors"][1]["error"]
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
        assert request.status_code == status.HTTP_404_NOT_FOUND
        assert request.data["error"] == (
            GenerateResetPasswordTOTPResp.resp_data["errors"][2]["error"]
        )
