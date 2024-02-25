import pytest

from django.urls import reverse

from util.error_resp_data import (
    AuthHeadersError,
    UserNotFoundError
)
from util.success_resp_data import GetSuccess


@pytest.mark.django_db
class TestUserInfo:
    def test_should_get_user_info(
            self,
            client,
            get_user_id,
            user_auth_headers
    ):
        request = client.get(
            reverse(
                "user_api:user_info",
                kwargs=get_user_id
            ),
            headers=user_auth_headers
        )
        assert request.status_code == GetSuccess().get_status()
        assert request.data["success"] == (
            GetSuccess().get_data()["success"]
        )

    def test_should_response_auth_headers_error(
            self,
            client,
            get_user_id
    ):
        request = client.get(
            reverse(
                "user_api:user_info",
                kwargs=get_user_id
            ),
        )

        assert request.status_code == AuthHeadersError().get_status()
        assert request.data["detail"] == (
            AuthHeadersError().get_data()["detail"]
        )

    def test_should_responce_user_not_found_error(
            self,
            client,
            get_wrong_user_id,
            user_auth_headers
    ):
        request = client.get(
            reverse(
                "user_api:user_info",
                kwargs=get_wrong_user_id
            ),
            headers=user_auth_headers
        )

        assert request.status_code == UserNotFoundError().get_status()
        assert request.data["user"] == (
            UserNotFoundError().get_data()["user"]
        )
