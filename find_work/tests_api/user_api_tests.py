import pytest
from django.urls import (
    reverse,
)

# Create your tests here.


@pytest.mark.django_db
class TestClassUser:

    # Tests for register api

    def test_should_register_user(
            self,
            mocker,
            client,
            data_for_test_register_user,
    ):
        mocker.patch(
            "django.core.mail.send_mail",
            return_value="return Response({'status':'Create'}, status=201)",
        )
        response = client.post(
            reverse("user_api:register"),
            data=data_for_test_register_user,
        )
        assert response.status_code == 201
        assert response.data.get("status") == "Create"

    def test_should_response_user_field_empty_error_in_register_api(
            self,
            client,
            data_for_test_user_field_empty_error,
    ):
        response = client.post(
            reverse("user_api:register"),
            data=data_for_test_user_field_empty_error,
        )
        assert response.status_code == 400
        assert response.data.get("error") == "UserFieldEmptyError"

    def test_should_response_profile_field_empty_error_in_register_api(
            self,
            client,
            data_for_test_profile_field_empty_error,
    ):
        response = client.post(
            reverse("user_api:register"),
            data=data_for_test_profile_field_empty_error,
        )
        assert response.status_code == 400
        assert response.data.get("error") == "ProfileFieldEmptyError"

    def test_should_response_email_already_exists_error_in_register_api(
            self,
            client,
            data_for_test_email_already_exists_error,
    ):
        response = client.post(
            reverse("user_api:register"),
            data=data_for_test_email_already_exists_error,
        )
        assert response.status_code == 409
        assert response.data.get("error") == "EmailAlreadyExists"

    def test_should_response_phone_number_already_exists_error_in_register_api(
            self,
            client,
            data_for_test_phone_number_already_exists_error,
    ):
        response = client.post(
            reverse("user_api:register"),
            data=data_for_test_phone_number_already_exists_error,
        )
        assert response.status_code == 409
        assert response.data.get("error") == "PhoneNumberAlreadyExistsError"

    # Tests for activate user api

    def test_should_activate_user(
            self,
            client,
            data_for_test_activate_user,
    ):
        kwargs = {"user_activation_uuid": data_for_test_activate_user}
        response = client.put(reverse("user_api:activate_user", kwargs=kwargs))

        assert response.status_code == 200
        assert response.data.get("status") == "Update"

    def test_should_response_user_already_active_error_in_activate_user_api(
            self,
            client,
            data_for_test_user_already_active_error,
    ):
        kwargs = {"user_activation_uuid": data_for_test_user_already_active_error}
        response = client.put(reverse("user_api:activate_user", kwargs=kwargs))

        assert response.status_code == 409
        assert response.data.get("error") == "UserAlreadyActiveError"

    # Tests for login api

    def test_should_login_user(
            self,
            client,
            data_for_test_login_user
    ):
        response = client.post(reverse("user_api:login"), data=data_for_test_login_user)
        assert response.status_code == 200

    def test_should_response_user_not_active_error_in_login_api(
            self,
            client,
            data_for_test_response_user_not_active_error
    ):
        response = client.post(
            reverse("user_api:login"),
            data=data_for_test_response_user_not_active_error,
        )
        assert response.status_code == 401

    def test_should_response_field_empty_error_in_login_api(
            self,
            client,
            data_for_test_response_field_empty_error
    ):
        response = client.post(
            reverse("user_api:login"),
            data=data_for_test_response_field_empty_error,
        )
        assert response.status_code == 400
