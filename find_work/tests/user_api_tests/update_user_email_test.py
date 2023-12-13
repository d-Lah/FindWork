import pytest

from django.urls import reverse

from rest_framework import status

from apps.response_success import ResponseUpdate
from apps.response_error import (
    ResponseEmailFieldEmptyError,
    ResponseEmailAlreadyExistsError,
)


@pytest.mark.django_db
class TestUpdateUserEmail:
    def test_should_update_user_email(
            self,
            client,
            user_auth_headers,
            data_for_test_should_update_user_email
    ):
        request = client.put(
            reverse("user_api:update_user_email"),
            headers=user_auth_headers,
            data=data_for_test_should_update_user_email
        )
        assert request.status_code == status.HTTP_200_OK
        assert request.data.get("status") == (
            ResponseUpdate.response_data["status"]
        )

    def test_should_response_auth_headers_error_in_update_user_email(
            self,
            client,
            data_for_test_should_update_user_email
    ):
        request = client.put(
            reverse("user_api:update_user_email"),
            data=data_for_test_should_update_user_email
        )
        assert request.status_code == status.HTTP_401_UNAUTHORIZED

    def test_should_response_email_already_exist_error(
            self,
            client,
            user_auth_headers,
            update_user_email_data_for_response_email_already_exist_error
    ):
        request = client.put(
            reverse("user_api:update_user_email"),
            headers=user_auth_headers,
            data=update_user_email_data_for_response_email_already_exist_error
        )
        assert request.status_code == status.HTTP_409_CONFLICT
        assert request.data.get("error") == (
            ResponseEmailAlreadyExistsError.response_data["error"]
        )

    def test_should_response_email_field_empty_error_in_update_user_email(
            self,
            client,
            user_auth_headers,
    ):
        request = client.put(
            reverse("user_api:update_user_email"),
            headers=user_auth_headers
        )
        assert request.status_code == status.HTTP_400_BAD_REQUEST
        assert request.data.get("error") == (
            ResponseEmailFieldEmptyError.response_data["error"]
        )
