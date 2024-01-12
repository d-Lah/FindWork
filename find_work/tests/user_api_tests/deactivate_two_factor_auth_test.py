import pytest

from django.urls import reverse

from rest_framework import status

from util.user_api_resp.deactivate_two_factor_auth_resp import (
    DeactivateTwoFactorAuthResp
)


@pytest.mark.django_db
class TestDeactivateTwoFactorAuth:
    def test_should_deactivate_two_factor_auth(
            self,
            client,
            data_to_deactivate_two_factor_auth
    ):
        request = client.put(
            reverse("user_api:deactivate_two_factor_auth"),
            headers=data_to_deactivate_two_factor_auth
        )

        assert request.status_code == status.HTTP_200_OK
        assert request.data["success"] == (
            DeactivateTwoFactorAuthResp.resp_data["successes"][0]["success"]
        )

    def test_should_response_auth_headers_error(
            self,
            client,
    ):
        request = client.put(
            reverse("user_api:deactivate_two_factor_auth"),
        )

        assert request.status_code == status.HTTP_401_UNAUTHORIZED

    def test_should_response_two_factor_auth_already_deactivated_error(
            self,
            client,
            data_to_deactivate_two_factor_auth_w_already_deactivated_user
    ):
        request = client.put(
            reverse("user_api:deactivate_two_factor_auth"),
            headers=data_to_deactivate_two_factor_auth_w_already_deactivated_user
        )

        assert request.status_code == status.HTTP_409_CONFLICT
        assert request.data["error"] == (
            DeactivateTwoFactorAuthResp.resp_data["errors"][0]["error"]
        )
