import pytest

from django.urls import reverse

from rest_framework import status

from util import error_resp_data
from util import success_resp_data


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

        assert request.status_code == success_resp_data.update["status_code"]
        assert request.data["detail"] == (
            success_resp_data.update["data"]["detail"]
        )

    def test_should_response_auth_headers_error(
            self,
            client,
    ):
        request = client.put(
            reverse("user_api:enable_two_factor_auth"),
        )

        assert request.status_code == status.HTTP_401_UNAUTHORIZED
        assert request.data["detail"] == error_resp_data.auth_headers

    def test_should_response_two_factor_auth_is_already_enabled_error(
            self,
            client,
            data_to_enable_two_factor_auth_w_already_enabled_auth
    ):
        request = client.put(
            reverse("user_api:enable_two_factor_auth"),
            headers=data_to_enable_two_factor_auth_w_already_enabled_auth
        )

        assert request.status_code == status.HTTP_409_CONFLICT
        assert request.data["detail"] == error_resp_data.already_enable
