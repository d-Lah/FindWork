import pytest

from django.urls import reverse

from rest_framework import status


@pytest.mark.django_db
class TestLoginUser:
    def test_should_login_user(
            self,
            client,
            data_for_login_user
    ):
        response = client.post(
            reverse("user_api:login_user"),
            data=data_for_login_user
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data["refresh"]
        assert response.data["access"]

    def test_should_response_user_not_active_error(
            self,
            client,
            login_user_data_for_response_user_not_active_error
    ):
        response = client.post(
            reverse("user_api:login_user"),
            data=login_user_data_for_response_user_not_active_error,
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["detail"] == (
            "No active account found with the given credentials"
        )

    def test_should_response_email_field_empty_error(
            self,
            client,
            login_user_data_for_response_email_field_empty_error
    ):
        response = client.post(
            reverse("user_api:login_user"),
            data=login_user_data_for_response_email_field_empty_error,
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["email"][0] == "This field may not be blank."

    def test_should_response_password_field_empty_error(
            self,
            client,
            login_user_data_for_response_password_field_empty_error
    ):
        response = client.post(
            reverse("user_api:login_user"),
            data=login_user_data_for_response_password_field_empty_error,
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["password"][0] == "This field may not be blank."

    def test_should_response_user_not_found_cause_wrong_email(
            self,
            client,
            login_user_data_for_response_user_not_found_error_cause_wrong_email,
    ):
        data = (
            login_user_data_for_response_user_not_found_error_cause_wrong_email
        )
        response = client.post(
            reverse("user_api:login_user"),
            data=data
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["detail"] == (
            "No active account found with the given credentials"
        )

    def test_should_response_user_not_found_cause_wrong_password(
            self,
            client,
            login_user_data_for_response_user_not_found_error_cause_wrong_password,
    ):
        data = (
            login_user_data_for_response_user_not_found_error_cause_wrong_password
        )
        response = client.post(
            reverse("user_api:login_user"),
            data=data
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["detail"] == (
            "No active account found with the given credentials"
        )
