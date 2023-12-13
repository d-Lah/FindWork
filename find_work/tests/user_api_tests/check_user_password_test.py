import pytest

from django.urls import reverse

from rest_framework import status

from apps.response_error import (
    ResponseWrongPasswordError,
    ResponsePasswordFieldEmptyError
)
from apps.response_success import ResponseValid


@pytest.mark.django_db
class TestCheckUserPassword:
    def test_should_check_user_password(
        self,
        client,
        user_auth_headers,
        check_user_password
    ):
        request = client.post(
            reverse("user_api:check_user_password"),
            headers=user_auth_headers,
            data=check_user_password
        )
        assert request.status_code == status.HTTP_200_OK
        assert request.data.get("status") == (
            ResponseValid.response_data["status"]
        )

    def test_should_response_auth_headers_error_in_check_user_password(
        self,
        client,
    ):
        request = client.post(
            reverse("user_api:check_user_password"),
        )
        assert request.status_code == status.HTTP_401_UNAUTHORIZED

    def test_should_response_password_field_empty_error_in_check_user_password(
        self,
        client,
        user_auth_headers
    ):
        request = client.post(
            reverse("user_api:check_user_password"),
            headers=user_auth_headers
        )
        assert request.status_code == status.HTTP_400_BAD_REQUEST
        assert request.data.get("error") == (
            ResponsePasswordFieldEmptyError.response_data["error"]
        )

    def test_should_response_wrong_password_error(
        self,
        client,
        user_auth_headers,
        check_user_password_response_wrong_password_error,
    ):
        request = client.post(
            reverse("user_api:check_user_password"),
            headers=user_auth_headers,
            data=check_user_password_response_wrong_password_error
        )
        assert request.status_code == status.HTTP_401_UNAUTHORIZED
        assert request.data.get("error") == (
            ResponseWrongPasswordError.response_data["error"]
        )
