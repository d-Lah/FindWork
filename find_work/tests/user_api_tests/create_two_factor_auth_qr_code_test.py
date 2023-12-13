import pytest

from django.urls import reverse

from rest_framework import status

from apps.response_success import ResponseGet


@pytest.mark.django_db
class TestGetTwoFactorAuthQRCode:
    def test_should_get_two_factor_auth_qr_code(
            self,
            client,
            user_auth_headers,
    ):
        request = client.post(
            reverse("user_api:create_2fa_qr_code"),
            headers=user_auth_headers,
        )
        assert request.status_code == status.HTTP_200_OK
        assert request.data.get("status") == (
            ResponseGet.response_data["status"]
        )

    def test_should_response_auth_headers_error(
            self,
            client,
    ):
        request = client.post(
            reverse("user_api:create_2fa_qr_code"),
        )
        assert request.status_code == status.HTTP_401_UNAUTHORIZED
