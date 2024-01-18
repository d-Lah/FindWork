import pytest

from django.urls import reverse

from rest_framework import status

from util.error_resp_data import (
    FieldsEmptyError,
    AuthHeadersError,
)
from util.success_resp_data import UpdateSuccess


@pytest.mark.django_db
class TestUpdatePassword:
    def test_should_update_password(
            self,
            client,
            mocker,
            user_auth_headers,
            data_to_update_password
    ):
        mocker.patch(
            "util.mail_sender.send_mail",
            return_value=True
        )

        request = client.put(
            reverse("user_api:update_password"),
            headers=user_auth_headers,
            data=data_to_update_password
        )
        assert request.status_code == UpdateSuccess().get_status()
        assert request.data["success"] == (
            UpdateSuccess().get_data()["success"]
        )

    def test_should_response_auth_headers_error(
            self,
            client,
    ):
        request = client.put(
            reverse("user_api:update_password"),
        )
        assert request.status_code == AuthHeadersError().get_status()

    def test_should_response_fields_empty_error(
            self,
            client,
            user_auth_headers
    ):
        request = client.put(
            reverse("user_api:update_password"),
            headers=user_auth_headers,
        )
        assert request.status_code == FieldsEmptyError().get_status()
        assert request.data["fields"] == (
            FieldsEmptyError().get_data()["fields"]
        )
