import pytest

from django.urls import reverse

from rest_framework import status

from apps.response_error import (
    ResponsePhoneNumberFieldEmptyError,
    ResponsePhoneNumberAlreadyExistsError,
)
from apps.response_success import ResponseUpdate


@pytest.mark.django_db
class TestupdateUserPhoneNumber:
    def test_should_update_user_phone_number(
            self,
            client,
            user_auth_headers,
            data_for_test_should_update_user_phone_number
    ):
        request = client.put(
            reverse("user_api:update_user_phone_number"),
            headers=user_auth_headers,
            data=data_for_test_should_update_user_phone_number
        )
        assert request.status_code == status.HTTP_200_OK
        assert request.data.get("status") == (
            ResponseUpdate.response_data["status"]
        )

    def test_should_response_auth_headers_error_in_update_user_phone_number(
            self,
            client,
            data_for_test_should_update_user_phone_number
    ):
        request = client.put(
            reverse("user_api:update_user_phone_number"),
            data=data_for_test_should_update_user_phone_number
        )
        assert request.status_code == status.HTTP_401_UNAUTHORIZED

    def test_should_response_phone_number_already_exiists_error(
            self,
            client,
            user_auth_headers,
            update_phone_number_data_for_respons_phone_number_already_exists
    ):
        request = client.put(
            reverse("user_api:update_user_phone_number"),
            headers=user_auth_headers,
            data=update_phone_number_data_for_respons_phone_number_already_exists
        )
        assert request.status_code == status.HTTP_409_CONFLICT
        assert request.data.get("error") == (
            ResponsePhoneNumberAlreadyExistsError.response_data["error"]
        )

    def test_should_response_phone_number_field_empty_error(
            self,
            client,
            user_auth_headers,
    ):
        request = client.put(
            reverse("user_api:update_user_phone_number"),
            headers=user_auth_headers,
        )
        assert request.status_code == status.HTTP_400_BAD_REQUEST
        assert request.data.get("error") == (
            ResponsePhoneNumberFieldEmptyError.response_data["error"]
        )
