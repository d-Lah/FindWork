import pytest

from django.urls import reverse

from rest_framework import status

from apps.response_success import ResponseUpdate
from apps.response_error import ResponsePasswordFieldEmptyError


@pytest.mark.django_db
class TestUpdateUserPassword:
    def test_should_update_user_password(
            self,
            client,
            mocker,
            user_auth_headers,
            data_for_test_should_update_user_password
    ):
        mocker.patch(
            "apps.mail_sender.send_mail",
            return_value=True
        )

        request = client.put(
            reverse("user_api:update_user_password"),
            headers=user_auth_headers,
            data=data_for_test_should_update_user_password
        )
        assert request.status_code == status.HTTP_200_OK
        assert request.data.get("status") == (
            ResponseUpdate.response_data["status"]
        )

    def test_should_response_auth_headers_error_in_update_user_password(
            self,
            client,
            data_for_test_should_update_user_password
    ):
        request = client.put(
            reverse("user_api:update_user_password"),
            data=data_for_test_should_update_user_password
        )
        assert request.status_code == status.HTTP_401_UNAUTHORIZED

    def test_should_response_password_field_empty_error_in_update_user_password(
            self,
            client,
            user_auth_headers
    ):
        request = client.put(
            reverse("user_api:update_user_password"),
            headers=user_auth_headers,
        )
        assert request.status_code == status.HTTP_400_BAD_REQUEST
        assert request.data.get("error") == (
            ResponsePasswordFieldEmptyError.response_data["error"]
        )
