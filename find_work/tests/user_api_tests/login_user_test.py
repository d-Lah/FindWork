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
        request = client.post(
            reverse("user_api:login_user"),
            data=data_to_login_user
        )
        assert request.status_code == status.HTTP_200_OK
        assert request.data["refresh"]
        assert request.data["access"]

    def test_should_response_user_not_active_error(
            self,
            client,
            data_to_login_user_w_not_active_user
    ):
        request = client.post(
            reverse("user_api:login_user"),
            data=data_to_login_user_w_not_active_user,
        )
        assert request.status_code == status.HTTP_401_UNAUTHORIZED
        assert request.data["detail"] == (
            "No active account found with the given credentials"
        )

    def test_should_response_fields_empty_error(
            self,
            client,
            data_to_login_user_wo_data
    ):
        request = client.post(
            reverse("user_api:login_user"),
            data=data_to_login_user_wo_data,
        )

        assert request.status_code == status.HTTP_400_BAD_REQUEST
        for field in request.data:
            assert request.data[field][0] == "This field may not be blank."

    def test_should_response_user_not_found_cause_wrong_email(
            self,
            client,
            data_to_login_user_w_wrong_email,
    ):
        request = client.post(
            reverse("user_api:login_user"),
            data=data_to_login_user_w_wrong_email
        )

        assert request.status_code == status.HTTP_401_UNAUTHORIZED
        assert request.data["detail"] == (
            "No active account found with the given credentials"
        )

    def test_should_response_user_not_found_cause_wrong_password(
            self,
            client,
            data_to_login_user_w_wrong_password
    ):
        request = client.post(
            reverse("user_api:login_user"),
            data=data_to_login_user_w_wrong_password
        )
        assert request.status_code == status.HTTP_401_UNAUTHORIZED
        assert request.data["detail"] == (
            "No active account found with the given credentials"
        )
