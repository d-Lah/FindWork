import pytest

from django.urls import reverse

from rest_framework import status

from util.success_resp_data import GetSuccess
from util.error_resp_data import AuthHeadersError


@pytest.mark.django_db
class TestProfileInfo:
    def test_should_get_profile_info(
            self,
            client,
            user_auth_headers
    ):
        request = client.get(
            reverse("user_api:profile_info"),
            headers=user_auth_headers
        )
        assert request.status_code == GetSuccess().get_status()
        assert request.data["success"] == (
            GetSuccess().get_data()["success"]
        )

    def test_should_response_auth_headers_error(
            self,
            client
    ):
        request = client.get(
            reverse("user_api:profile_info"),
        )
        assert request.status_code == AuthHeadersError().get_status()
