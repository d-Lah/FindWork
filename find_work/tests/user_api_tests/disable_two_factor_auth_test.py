import pytest

from django.urls import reverse

from util.error_resp_data import (
    AuthHeadersError,
    TwoFactorAuthAlreadyDisabledError
)
from util.success_resp_data import UpdateSuccess


@pytest.mark.django_db
class TestDeactivateTwoFactorAuth:
    def test_should_disable_two_factor_auth(
            self,
            client,
            data_to_disable_two_factor_auth
    ):
        request = client.put(
            reverse("user_api:disable_two_factor_auth"),
            headers=data_to_disable_two_factor_auth
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
            reverse("user_api:disable_two_factor_auth"),
        )

        assert request.status_code == AuthHeadersError().get_status()
        assert request.data["detail"] == (
            AuthHeadersError().get_data()["detail"]
        )

    def test_should_response_two_factor_auth_is_already_disabled_error(
            self,
            client,
            data_to_disable_two_factor_auth_w_already_disabled_auth
    ):
        request = client.put(
            reverse("user_api:disable_two_factor_auth"),
            headers=data_to_disable_two_factor_auth_w_already_disabled_auth
        )

        assert request.status_code == (
            TwoFactorAuthAlreadyDisabledError().get_status()
        )
        assert request.data["user"] == (
            TwoFactorAuthAlreadyDisabledError().get_data()["user"]
        )
