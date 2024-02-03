import pytest

from django.urls import reverse

from util.error_resp_data import (
    AuthHeadersError,
    FieldsEmptyError,
    InvalidEmailAdressError,
    EmailAlreadyExistsError,
)
from util.success_resp_data import UpdateSuccess


@pytest.mark.django_db
class TestUpdateEmail:
    def test_should_update_email(
            self,
            client,
            user_auth_headers,
            data_to_update_email
    ):
        request = client.put(
            reverse("user_api:update_email"),
            headers=user_auth_headers,
            data=data_to_update_email
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
            reverse("user_api:update_email"),
        )
        assert request.status_code == AuthHeadersError().get_status()

    def test_should_response_fields_empty_error(
            self,
            client,
            user_auth_headers,
            data_to_update_email_wo_email
    ):
        request = client.put(
            reverse("user_api:update_email"),
            headers=user_auth_headers,
            data=data_to_update_email_wo_email
        )
        assert request.status_code == FieldsEmptyError().get_status()
        assert request.data["fields"] == (
            FieldsEmptyError().get_data()["fields"]
        )

    def test_should_response_invalid_email_error(
            self,
            client,
            user_auth_headers,
            data_to_update_email_w_invalid_email
    ):
        request = client.put(
            reverse("user_api:update_email"),
            headers=user_auth_headers,
            data=data_to_update_email_w_invalid_email
        )
        assert request.status_code == InvalidEmailAdressError().get_status()
        assert request.data["email"] == (
            InvalidEmailAdressError().get_data()["email"]
        )

    def test_should_response_email_already_exist_error(
            self,
            client,
            user_auth_headers,
            data_to_update_email_w_already_exists_email
    ):
        request = client.put(
            reverse("user_api:update_email"),
            headers=user_auth_headers,
            data=data_to_update_email_w_already_exists_email
        )
        assert request.status_code == EmailAlreadyExistsError().get_status()
        assert request.data["email"] == (
            EmailAlreadyExistsError().get_data()["email"]
        )
