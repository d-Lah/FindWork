import pytest

from django.urls import reverse

from rest_framework import status

from util.user_api_resp.activate_two_factor_auth_resp import (
    ActivateTwoFactorAuthResp
)


@pytest.mark.django_db
class TestActivateTwoFactorAuth:
    def test_should_activate_two_factor_auth(
            self,
            client,
            user_auth_headers
    ):
        request = client.put(
            reverse("user_api:activate_two_factor_auth"),
            headers=user_auth_headers
        )

        assert request.status_code == status.HTTP_200_OK
        assert request.data["success"] == (
            ActivateTwoFactorAuthResp.resp_data["successes"][0]["success"]
        )

    def test_should_response_auth_headers_error(
            self,
            client,
    ):
        request = client.put(
            reverse("user_api:activate_two_factor_auth"),
        )

        assert request.status_code == status.HTTP_401_UNAUTHORIZED

    def test_should_response_two_factor_auth_already_activated_error(
            self,
            client,
            data_to_activate_two_factor_auth_w_already_activated_user
    ):
        request = client.put(
            reverse("user_api:activate_two_factor_auth"),
            headers=data_to_activate_two_factor_auth_w_already_activated_user
        )

        assert request.status_code == status.HTTP_409_CONFLICT
        assert request.data["error"] == (
            ActivateTwoFactorAuthResp.resp_data["errors"][0]["error"]
        )
