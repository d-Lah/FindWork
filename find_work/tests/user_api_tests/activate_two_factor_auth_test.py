import pytest

from django.urls import reverse

from rest_framework import status

from apps.response_success import ResponseUpdate
from apps.response_error import ResponseTwoFactorAuthAlreadyActiveError


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
        assert request.data.get("status") == (
            ResponseUpdate.response_data["status"]
        )

    def test_should_response_auth_headers_error_in_activate_two_factor_auth(
            self,
            client,
    ):
        request = client.put(
            reverse("user_api:activate_two_factor_auth"),
        )

        assert request.status_code == status.HTTP_401_UNAUTHORIZED

    def test_should_response_two_factor_auth_already_active_error(
            self,
            client,
            data_for_response_two_factor_auth_already_active_error
    ):
        request = client.put(
            reverse("user_api:activate_two_factor_auth"),
            headers=data_for_response_two_factor_auth_already_active_error
        )

        assert request.status_code == status.HTTP_409_CONFLICT
        assert request.data.get("error") == (
            ResponseTwoFactorAuthAlreadyActiveError.response_data["error"]
        )
