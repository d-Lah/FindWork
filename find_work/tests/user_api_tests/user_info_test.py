import pytest

from django.urls import reverse

from rest_framework import status

from apps.response_success import ResponseGet


@pytest.mark.django_db
class TestUserInfo:
    def test_should_get_user_info(
            self,
            client,
            user_auth_headers
    ):
        request = client.get(
            reverse("user_api:user_info"),
            headers=user_auth_headers
        )
        assert request.status_code == status.HTTP_200_OK
        assert request.data.get("status") == (
            ResponseGet.response_data["status"]
        )

    def test_should_response_auth_headers_error_in_user_info(
            self,
            client
    ):
        request = client.get(
            reverse("user_api:user_info"),
        )
        assert request.status_code == status.HTTP_401_UNAUTHORIZED
