import pytest

from django.urls import reverse

from rest_framework import status

from apps.response_success import ResponseUpdate
from apps.response_error import (
    ResponseUserNotFoundError,
    ResponseEmailFieldEmptyError,
    ResponsePasswordFieldEmptyError,
)


@pytest.mark.django_db
class TestResetUserPassword:
    def test_should_reset_user_password(
            self,
            client,
            data_to_reset_user_password
    ):
        request = client.put(
            reverse("user_api:reset_user_password"),
            data=data_to_reset_user_password
        )
        assert request.status_code == status.HTTP_200_OK
        assert request.data.get("status") == (
            ResponseUpdate.response_data["status"]
        )

    def test_should_response_email_field_empty_error(
            self,
            client,
            reset_user_password_data_to_response_email_field_empty_error
    ):
        request = client.put(
            reverse("user_api:reset_user_password"),
            data=reset_user_password_data_to_response_email_field_empty_error
        )
        assert request.status_code == status.HTTP_400_BAD_REQUEST
        assert request.data.get("error") == (
            ResponseEmailFieldEmptyError.response_data["error"]
        )

    def test_should_response_password_field_empty_error(
            self,
            client,
            reset_user_password_data_to_response_password_field_empty_error
    ):
        request = client.put(
            reverse("user_api:reset_user_password"),
            data=reset_user_password_data_to_response_password_field_empty_error

        )
        assert request.status_code == status.HTTP_400_BAD_REQUEST
        assert request.data.get("error") == (
            ResponsePasswordFieldEmptyError.response_data["error"]
        )

    def test_should_response_user_not_found_error(
            self,
            client,
            reset_user_password_data_to_response_user_not_found_error
    ):
        request = client.put(
            reverse("user_api:reset_user_password"),
            data=reset_user_password_data_to_response_user_not_found_error
        )
        assert request.status_code == status.HTTP_404_NOT_FOUND
        assert request.data.get("error") == (
            ResponseUserNotFoundError.response_data["error"]
        )
