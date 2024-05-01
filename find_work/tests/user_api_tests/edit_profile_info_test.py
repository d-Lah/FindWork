import pytest

from django.urls import reverse

from rest_framework import status

from util import error_resp_data
from util import success_resp_data


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

        assert request.status_code == success_resp_data.update["status_code"]
        assert request.data["detail"] == (
            success_resp_data.update["data"]["detail"]
        )

    def test_should_response_auth_headers_error(
            self,
            client,
    ):
        request = client.put(
            reverse("user_api:edit_profile_info"),
        )

        assert request.status_code == status.HTTP_401_UNAUTHORIZED
        assert request.data["detail"] == error_resp_data.auth_headers

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

        assert request.status_code == status.HTTP_400_BAD_REQUEST
        for key in request.data:
            assert request.data[key][0] == error_resp_data.field_is_blank
