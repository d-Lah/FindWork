import pytest

from django.urls import reverse

from util.success_resp_data import UpdateSuccess
from util.error_resp_data import (
    AuthHeadersError,
    TwoFactorAuthAlreadyEnabledError,
)


@pytest.mark.django_db
class TestEnableTwoFactorAuth:
    def test_should_enable_two_factor_auth(
            self,
            client,
            user_auth_headers
    ):
        request = client.put(
            reverse("user_api:enable_two_factor_auth"),
            headers=user_auth_headers
        )

        assert request.status_code == UpdateSuccess().get_status()
        assert request.data["success"] == (
            UpdateSuccess().get_data()["success"]
        )

    def test_should_response_auth_headers_error(
            self,
            client,
    ):
        request = client.put(
            reverse("user_api:enable_two_factor_auth"),
        )

        assert request.status_code == AuthHeadersError().get_status()

    def test_should_response_two_factor_auth_is_already_enabled_error(
            self,
            client,
            data_to_enable_two_factor_auth_w_already_enabled_auth
    ):
        request = client.put(
            reverse("user_api:enable_two_factor_auth"),
            headers=data_to_enable_two_factor_auth_w_already_enabled_auth
        )

        assert request.status_code == (
            TwoFactorAuthAlreadyEnabledError().get_status()
        )
        assert request.data["user"] == (
            TwoFactorAuthAlreadyEnabledError().get_data()["user"]
        )
