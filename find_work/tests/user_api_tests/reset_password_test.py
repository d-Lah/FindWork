import pytest

from django.urls import reverse

from rest_framework import status

from util.user_api_resp.reset_password_resp import ResetPasswordResp


@pytest.mark.django_db
class TestResetPassword:
    def test_should_reset_password(
            self,
            client,
            data_to_reset_password
    ):
        request = client.put(
            reverse("user_api:reset_password"),
            data=data_to_reset_password
        )
        assert request.status_code == status.HTTP_200_OK
        assert request.data["success"] == (
            ResetPasswordResp.resp_data["successes"][0]["success"]
        )

    def test_should_response_fields_empty_error(
            self,
            client,
            data_to_reset_password_wo_data
    ):
        request = client.put(
            reverse("user_api:reset_password"),
            data=data_to_reset_password_wo_data
        )
        assert request.status_code == status.HTTP_400_BAD_REQUEST
        assert request.data["error"] == (
            ResetPasswordResp.resp_data["errors"][0]["error"]
        )

    def test_should_response_invalid_email_error(
            self,
            client,
            data_to_reset_password_w_invalid_email
    ):
        request = client.put(
            reverse("user_api:reset_password"),
            data=data_to_reset_password_w_invalid_email

        )
        assert request.status_code == status.HTTP_400_BAD_REQUEST
        assert request.data["error"] == (
            ResetPasswordResp.resp_data["errors"][1]["error"]
        )

    def test_should_response_not_found_error(
            self,
            client,
            data_to_reset_password_w_wrong_email
    ):
        request = client.put(
            reverse("user_api:reset_password"),
            data=data_to_reset_password_w_wrong_email
        )
        assert request.status_code == status.HTTP_404_NOT_FOUND
        assert request.data["error"] == (
            ResetPasswordResp.resp_data["errors"][2]["error"]
        )
