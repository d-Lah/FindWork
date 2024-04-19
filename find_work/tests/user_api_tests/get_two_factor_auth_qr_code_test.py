import pytest

from django.urls import reverse

from rest_framework import status

from util import error_resp_data
from util import success_resp_data


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

        assert request.status_code == success_resp_data.get["status_code"]
        assert request.data["detail"] == (
            success_resp_data.get["data"]["detail"]
        )

    def test_should_response_auth_headers_error(
            self,
            client,
    ):
        request = client.post(
            reverse("user_api:get_two_factor_auth_qr_code"),
        )

        assert request.status_code == status.HTTP_401_UNAUTHORIZED
        assert request.data["detail"] == error_resp_data.auth_headers
