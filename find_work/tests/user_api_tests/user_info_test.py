import pytest

from django.urls import reverse

from rest_framework import status

from util.user_api_resp.user_info_resp import UserInfoResp


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
        assert request.data["success"] == (
            UserInfoResp.resp_data["successes"][0]["success"]
        )

    def test_should_response_auth_headers_error(
            self,
            client
    ):
        request = client.get(
            reverse("user_api:user_info"),
        )
        assert request.status_code == status.HTTP_401_UNAUTHORIZED
