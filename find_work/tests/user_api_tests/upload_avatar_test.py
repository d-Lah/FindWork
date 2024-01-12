import pytest

from django.urls import reverse

from rest_framework import status

from user.models import (
    Profile,
    UserAvatar,
)

from util.user_api_resp.upload_avatar_resp import UploadAvatarResp


@pytest.mark.django_db
class TestUploadAvatar:
    def test_should_upload_avatar(
            self,
            client,
            mocker,
            user_auth_headers,
            data_to_upload_avatar
    ):
        mocker.patch.object(
            Profile,
            "save",
            return_value="return ResponseUpload().get_response()")
        mocker.patch.object(
            UserAvatar,
            "save",
            return_value="return ResponseUpload().get_response()"
        )

        request = client.post(
            reverse("user_api:upload_avatar"),
            headers=user_auth_headers,
            data=data_to_upload_avatar
        )
        assert request.status_code == status.HTTP_201_CREATED
        assert request.data["success"] == (
            UploadAvatarResp.resp_data["successes"][0]["success"]
        )

    def test_should_response_auth_headers_error(
            self,
            client,
            data_to_upload_avatar_wo_image
    ):
        request = client.post(
            reverse("user_api:upload_avatar"),
            data=data_to_upload_avatar_wo_image
        )
        assert request.status_code == status.HTTP_401_UNAUTHORIZED

    def test_should_response_avatar_fields_empty_error(
            self,
            client,
            user_auth_headers
    ):
        request = client.post(
            reverse("user_api:upload_avatar"),
            headers=user_auth_headers,
        )
        assert request.status_code == status.HTTP_400_BAD_REQUEST
        assert request.data["error"] == (
            UploadAvatarResp.resp_data["errors"][0]["error"]
        )

    def test_should_response_image_size_too_large_error(
            self,
            client,
            user_auth_headers,
            data_to_upload_avatar_w_big_file
    ):
        request = client.post(
            reverse("user_api:upload_avatar"),
            headers=user_auth_headers,
            data=data_to_upload_avatar_w_big_file
        )
        assert request.status_code == status.HTTP_413_REQUEST_ENTITY_TOO_LARGE
        assert request.data["error"] == (
            UploadAvatarResp.resp_data["errors"][1]["error"]
        )

    def test_should_response_invalid_image_ext_error(
            self,
            client,
            user_auth_headers,
            data_to_upload_avatar_w_file_w_invalid_ext
    ):
        request = client.post(
            reverse("user_api:upload_avatar"),
            headers=user_auth_headers,
            data=data_to_upload_avatar_w_file_w_invalid_ext
        )
        assert request.status_code == status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
        assert request.data["error"] == (
            UploadAvatarResp.resp_data["errors"][2]["error"]
        )
