import pytest

from django.urls import reverse

from rest_framework import status


@pytest.mark.django_db
class TestLoginUser:
    def test_should_login_user(
            self,
            client,
            data_to_login_user
    ):
        response = client.post(
            reverse("user_api:login_user"),
            data=data_to_login_user
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data["refresh"]
        assert response.data["access"]

    def test_should_response_user_not_active_error(
            self,
            client,
            data_to_login_user_w_not_active_user
    ):
        response = client.post(
            reverse("user_api:login_user"),
            data=data_to_login_user_w_not_active_user,
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["detail"] == (
            "No active account found with the given credentials"
        )

    def test_should_response_email_field_empty_error(
            self,
            client,
            data_to_login_user_wo_email
    ):
        response = client.post(
            reverse("user_api:login_user"),
            data=data_to_login_user_wo_email,
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["email"][0] == "This field may not be blank."

    def test_should_response_password_field_empty_error(
            self,
            client,
            data_to_login_user_wo_password
    ):
        response = client.post(
            reverse("user_api:login_user"),
            data=data_to_login_user_wo_password,
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["password"][0] == "This field may not be blank."

    def test_should_response_user_not_found_cause_wrong_email(
            self,
            client,
            data_to_login_user_w_wrong_email,
    ):
        response = client.post(
            reverse("user_api:login_user"),
            data=data_to_login_user_w_wrong_email
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["detail"] == (
            "No active account found with the given credentials"
        )

    def test_should_response_user_not_found_cause_wrong_password(
            self,
            client,
            data_to_login_user_w_wrong_password
    ):
        response = client.post(
            reverse("user_api:login_user"),
            data=data_to_login_user_w_wrong_password
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["detail"] == (
            "No active account found with the given credentials"
        )
