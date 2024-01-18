import pytest

from django.urls import reverse

from util.error_resp_data import (
    FieldsEmptyError,
    UserNotFoundError,
    InvalidEmailAdressError,
)
from util.success_resp_data import UpdateSuccess


@pytest.mark.django_db
class TestResetPassword:
    def test_should_reset_password(
            self,
            client,
            data_to_reset_password
    ):
        request = client.put(
            reverse("user_api:reset_password"),
            data=data_to_reset_password
        )
        assert request.status_code == UpdateSuccess().get_status()
        assert request.data["success"] == (
            UpdateSuccess().get_data()["success"]
        )

    def test_should_response_fields_empty_error(
            self,
            client,
            data_to_reset_password_wo_data
    ):
        request = client.put(
            reverse("user_api:reset_password"),
            data=data_to_reset_password_wo_data
        )
        assert request.status_code == FieldsEmptyError().get_status()
        assert request.data["fields"] == (
            FieldsEmptyError().get_data()["fields"]
        )

    def test_should_response_invalid_email_error(
            self,
            client,
            data_to_reset_password_w_invalid_email
    ):
        request = client.put(
            reverse("user_api:reset_password"),
            data=data_to_reset_password_w_invalid_email

        )
        assert request.status_code == InvalidEmailAdressError().get_status()
        assert request.data["email"] == (
            InvalidEmailAdressError().get_data()["email"]
        )

    def test_should_response_not_found_error(
            self,
            client,
            data_to_reset_password_w_wrong_email
    ):
        request = client.put(
            reverse("user_api:reset_password"),
            data=data_to_reset_password_w_wrong_email
        )
        assert request.status_code == UserNotFoundError().get_status()
        assert request.data["email"] == (
            UserNotFoundError().get_data()["email"]
        )
