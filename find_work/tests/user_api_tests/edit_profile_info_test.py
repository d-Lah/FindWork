import pytest

from django.urls import reverse

from rest_framework import status

from util.error_resp_data import (
    AuthHeadersError,
    FieldsEmptyError,
)
from util.success_resp_data import UpdateSuccess


@pytest.mark.django_db
class TestEditProfileInfo:
    def test_should_edit_profile_info(
            self,
            client,
            user_auth_headers,
            data_to_edit_profile_info
    ):
        request = client.put(
            reverse("user_api:edit_profile_info"),
            headers=user_auth_headers,
            data=data_to_edit_profile_info
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
            reverse("user_api:edit_profile_info"),
        )
        assert request.status_code == AuthHeadersError().get_status()

    def test_should_response_fields_empty_error(
            self,
            client,
            user_auth_headers,
            data_to_edit_profile_info_wo_data
    ):
        request = client.put(
            reverse("user_api:edit_profile_info"),
            headers=user_auth_headers,
            data=data_to_edit_profile_info_wo_data
        )
        assert request.status_code == FieldsEmptyError().get_status()
        assert request.data["fields"] == (
            FieldsEmptyError().get_data()["fields"]
        )
