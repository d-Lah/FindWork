import pytest

from django.urls import reverse

from rest_framework import status

from apps.response_error import (
    ResponseUserFieldEmptyError,
    ResponseProfileFieldEmptyError,
    ResponseEmailAlreadyExistsError,
    ResponsePhoneNumberAlreadyExistsError,
)
from apps.response_success import ResponseCreate


@pytest.mark.django_db
class TestRegisterNewUser:
    def test_should_register_new_user(
            self,
            mocker,
            client,
            data_for_test_register_user,
    ):
        mocker.patch(
            "apps.mail_sender.send_mail",
            return_value=True
        )

        response = client.post(
            reverse("user_api:register_new_user"),
            data=data_for_test_register_user
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data.get("status") == (
            ResponseCreate.response_data["status"]
        )

    def test_should_response_email_field_empty_error(
            self,
            client,
            register_new_user_data_for_response_email_field_empty_error,
    ):
        response = client.post(
            reverse("user_api:register_new_user"),
            data=register_new_user_data_for_response_email_field_empty_error,
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data.get("error") == (
            ResponseUserFieldEmptyError.response_data["error"]
        )

    def test_should_response_phone_number_field_empty_error(
            self,
            client,
            register_new_user_data_for_response_phone_number_field_empty_error,
    ):
        response = client.post(
            reverse("user_api:register_new_user"),
            data=register_new_user_data_for_response_phone_number_field_empty_error,
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data.get("error") == (
            ResponseUserFieldEmptyError.response_data["error"]
        )

    def test_should_response_password_field_empty_error(
            self,
            client,
            register_new_user_data_for_response_password_field_empty_error,
    ):
        response = client.post(
            reverse("user_api:register_new_user"),
            data=register_new_user_data_for_response_password_field_empty_error,
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data.get("error") == (
            ResponseUserFieldEmptyError.response_data["error"]
        )

    def test_should_response_is_employer_field_empty_error(
            self,
            client,
            register_new_user_data_for_response_is_employer_field_empty_error,
    ):
        response = client.post(
            reverse("user_api:register_new_user"),
            data=register_new_user_data_for_response_is_employer_field_empty_error,
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data.get("error") == (
            ResponseUserFieldEmptyError.response_data["error"]
        )

    def test_should_response_is_employee_field_empty_error(
            self,
            client,
            register_new_user_data_for_response_is_employee_field_empty_error,
    ):
        response = client.post(
            reverse("user_api:register_new_user"),
            data=register_new_user_data_for_response_is_employee_field_empty_error,
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data.get("error") == (
            ResponseUserFieldEmptyError.response_data["error"]
        )

    def test_should_response_first_name_field_empty_error(
            self,
            client,
            register_new_user_data_for_response_first_name_field_empty_error,
    ):
        response = client.post(
            reverse("user_api:register_new_user"),
            data=register_new_user_data_for_response_first_name_field_empty_error,
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data.get("error") == (
            ResponseProfileFieldEmptyError.response_data["error"]
        )

    def test_should_response_second_name_field_empty_error(
            self,
            client,
            register_new_user_data_for_response_second_name_field_empty_error,
    ):
        response = client.post(
            reverse("user_api:register_new_user"),
            data=register_new_user_data_for_response_second_name_field_empty_error,
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data.get("error") == (
            ResponseProfileFieldEmptyError.response_data["error"]
        )

    def test_should_response_email_already_exists_error(
            self,
            client,
            data_for_test_email_already_exists_error,
    ):
        response = client.post(
            reverse("user_api:register_new_user"),
            data=data_for_test_email_already_exists_error,
        )
        assert response.status_code == status.HTTP_409_CONFLICT
        assert response.data.get("error") == (
            ResponseEmailAlreadyExistsError.response_data["error"]
        )

    def test_should_response_phone_number_already_exists_error(
            self,
            client,
            data_for_test_phone_number_already_exists_error,
    ):
        response = client.post(
            reverse("user_api:register_new_user"),
            data=data_for_test_phone_number_already_exists_error,
        )
        assert response.status_code == status.HTTP_409_CONFLICT
        assert response.data.get("error") == (
            ResponsePhoneNumberAlreadyExistsError.response_data["error"]
        )
