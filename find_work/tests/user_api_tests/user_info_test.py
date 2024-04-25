import pytest

from django.urls import reverse

from rest_framework import status

from util import error_resp_data
from util import success_resp_data


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

        assert request.status_code == success_resp_data.get["status_code"]
        assert request.data["detail"] == (
            success_resp_data.get["data"]["detail"]
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

        assert request.status_code == status.HTTP_401_UNAUTHORIZED
        assert request.data["detail"] == error_resp_data.auth_headers

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

        assert request.status_code == status.HTTP_404_NOT_FOUND
        assert request.data["detail"] == error_resp_data.user_not_found
