import pytest

from django.urls import reverse

from rest_framework import status

from util.success_resp_data import GetSuccess
from util.error_resp_data import AuthHeadersError


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
        assert request.status_code == GetSuccess().get_status()
        assert request.data["success"] == GetSuccess().get_data()["success"]

    def test_should_response_auth_headers_error(
            self,
            client,
    ):
        request = client.post(
            reverse("user_api:get_two_factor_auth_qr_code"),
        )
        assert request.status_code == AuthHeadersError().get_status()
