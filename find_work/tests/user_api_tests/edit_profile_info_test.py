import pytest

from django.urls import reverse

from rest_framework import status

from apps.response_success import ResponseUpdate
from apps.response_error import ResponseProfileFieldEmptyError


@pytest.mark.django_db
class TestEditProfileInfo:
    def test_should_edit_profile_info(
            self,
            client,
            user_auth_headers,
            data_for_test_should_edit_profile_info
    ):
        request = client.put(
            reverse("user_api:edit_profile_info"),
            headers=user_auth_headers,
            data=data_for_test_should_edit_profile_info
        )
        assert request.status_code == status.HTTP_200_OK
        assert request.data.get("status") == (
            ResponseUpdate.response_data["status"]
        )

    def test_should_response_auth_headers_error(
            self,
            client,
    ):
        request = client.put(
            reverse("user_api:edit_profile_info"),
        )
        assert request.status_code == status.HTTP_401_UNAUTHORIZED

    def test_should_response_first_name_field_empty_error(
            self,
            client,
            user_auth_headers,
            edit_profile_info_data_for_response_first_name_field_empty_error
    ):
        data = edit_profile_info_data_for_response_first_name_field_empty_error
        request = client.put(
            reverse("user_api:edit_profile_info"),
            headers=user_auth_headers,
            data=data
        )
        assert request.status_code == status.HTTP_400_BAD_REQUEST
        assert request.data.get("error") == (
            ResponseProfileFieldEmptyError.response_data["error"]
        )

    def test_should_response_second_name_field_empty_error(
            self,
            client,
            user_auth_headers,
            edit_profile_info_data_for_response_second_name_field_empty_error
    ):
        data = edit_profile_info_data_for_response_second_name_field_empty_error
        request = client.put(
            reverse("user_api:edit_profile_info"),
            headers=user_auth_headers,
            data=data
        )
        assert request.status_code == status.HTTP_400_BAD_REQUEST
        assert request.data.get("error") == (
            ResponseProfileFieldEmptyError.response_data["error"]
        )
