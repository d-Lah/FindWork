import pytest

from django.urls import reverse

from rest_framework import status

from util.user_api_resp.get_two_factor_auth_qr_code_resp import (
    GetTwoFacteorAuthQRCodeResp
)


@pytest.mark.django_db
class TestGetTwoFactorAuthQRCode:
    def test_should_get_two_factor_auth_qr_code(
            self,
            client,
            user_auth_headers,
    ):
        request = client.post(
            reverse("user_api:get_two_factor_auth_qr_code"),
            headers=user_auth_headers,
        )
        assert request.status_code == status.HTTP_200_OK
        assert request.data["success"] == (
            GetTwoFacteorAuthQRCodeResp.resp_data["successes"][0]["success"]
        )

    def test_should_response_auth_headers_error(
            self,
            client,
    ):
        request = client.post(
            reverse("user_api:get_two_factor_auth_qr_code"),
        )
        assert request.status_code == status.HTTP_401_UNAUTHORIZED
