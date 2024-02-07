import pytest

from django.urls import reverse

from rest_framework import status

from util.error_resp_data import (
    AuthHeadersError,
    FieldsEmptyError,
    WrongPasswordError
)
from util.success_resp_data import ValidateSuccess


@pytest.mark.django_db
class TestValidatePassword:
    def test_should_validate_password(
        self,
        client,
        user_auth_headers,
        data_to_validate_password
    ):
        request = client.post(
            reverse("user_api:validate_password"),
            headers=user_auth_headers,
            data=data_to_validate_password
        )
        assert request.status_code == ValidateSuccess().get_status()
        assert request.data["success"] == (
            ValidateSuccess().get_data()["success"]
        )

    def test_should_response_auth_headers_error(
        self,
        client,
    ):
        request = client.post(
            reverse("user_api:validate_password"),
        )

        assert request.status_code == AuthHeadersError().get_status()
        assert request.data["detail"] == (
            AuthHeadersError().get_data()["detail"]
        )

    def test_should_response_fields_empty_error(
        self,
        client,
        user_auth_headers
    ):
        request = client.post(
            reverse("user_api:validate_password"),
            headers=user_auth_headers
        )
        assert request.status_code == FieldsEmptyError().get_status()
        assert request.data["fields"] == (
            FieldsEmptyError().get_data()["fields"]
        )

    def test_should_response_wrong_password_error(
        self,
        client,
        user_auth_headers,
        data_to_validate_password_w_wrong_password,
    ):
        request = client.post(
            reverse("user_api:validate_password"),
            headers=user_auth_headers,
            data=data_to_validate_password_w_wrong_password
        )
        assert request.status_code == WrongPasswordError().get_status()
        assert request.data["password"] == (
            WrongPasswordError().get_data()["password"]
        )
