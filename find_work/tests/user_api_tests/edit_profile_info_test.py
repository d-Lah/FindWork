import pytest

from django.urls import reverse

from rest_framework import status

from util.user_api_resp.edit_profile_info_resp import EditProfileInfoResp


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
        assert request.status_code == status.HTTP_200_OK
        assert request.data["success"] == (
            EditProfileInfoResp.resp_data["successes"][0]["success"]
        )

    def test_should_response_auth_headers_error(
            self,
            client,
    ):
        request = client.put(
            reverse("user_api:edit_profile_info"),
        )
        assert request.status_code == status.HTTP_401_UNAUTHORIZED

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
        assert request.data["error"] == (
            EditProfileInfoResp.resp_data["errors"][0]["error"]
        )
