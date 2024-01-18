import pytest

from django.urls import reverse

from util.error_resp_data import (
    FieldsEmptyError,
    InvalidEmailAdressError,
    EmailAlreadyExistsError,
)
from util.success_resp_data import CreateSuccess


@pytest.mark.django_db
class TestRegisterNewUser:
    def test_should_register_new_user(
            self,
            mocker,
            client,
            data_to_register_new_user
    ):
        mocker.patch(
            "util.mail_sender.send_mail",
            return_value=True
        )
        response = client.post(
            reverse("user_api:register_new_user"),
            data=data_to_register_new_user
        )
        assert response.status_code == CreateSuccess().get_status()
        assert response.data["success"] == (
            CreateSuccess().get_data()["success"]
        )

    def test_should_response_fields_empty_error(
            self,
            client,
            data_to_register_new_user_wo_data
    ):
        response = client.post(
            reverse("user_api:register_new_user"),
            data=data_to_register_new_user_wo_data
        )
        assert response.status_code == FieldsEmptyError().get_status()
        assert response.data["fields"] == (
            FieldsEmptyError().get_data()["fields"]
        )

    def test_should_response_invalid_email_error(
            self,
            client,
            data_to_register_new_user_w_invalid_email
    ):
        response = client.post(
            reverse("user_api:register_new_user"),
            data=data_to_register_new_user_w_invalid_email
        )
        assert response.status_code == InvalidEmailAdressError().get_status()
        assert response.data["email"] == (
            InvalidEmailAdressError().get_data()["email"]
        )

    def test_should_response_email_already_exists_error(
            self,
            client,
            data_to_register_new_user_w_already_exists_email
    ):
        response = client.post(
            reverse("user_api:register_new_user"),
            data=data_to_register_new_user_w_already_exists_email
        )
        assert response.status_code == EmailAlreadyExistsError().get_status()
        assert response.data["email"] == (
            EmailAlreadyExistsError().get_data()["email"]
        )
