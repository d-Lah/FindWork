import pytest

from django.urls import reverse

from rest_framework import status

from user.models import (
    Profile,
    UserAvatar,
)

from util import error_resp_data
from util import success_resp_data


@pytest.mark.django_db
class TestUploadUserAvatar:
    def test_should_upload_avatar(
            self,
            client,
            mocker,
            user_auth_headers,
            data_to_upload_user_avatar
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
            reverse("user_api:upload_user_avatar"),
            headers=user_auth_headers,
            data=data_to_upload_user_avatar
        )

        assert request.status_code == success_resp_data.upload["status_code"]
        assert request.data["detail"] == (
            success_resp_data.upload["data"]["detail"]
        )

    def test_should_response_auth_headers_error(
            self,
            client,
    ):
        request = client.post(
            reverse("user_api:upload_user_avatar"),
        )

        assert request.status_code == status.HTTP_401_UNAUTHORIZED
        assert request.data["detail"] == error_resp_data.auth_headers

    def test_should_response_avatar_file_not_submitted_error(
            self,
            client,
            user_auth_headers,
            data_to_upload_user_avatar_wo_data
    ):
        request = client.post(
            reverse("user_api:upload_user_avatar"),
            headers=user_auth_headers,
            data=data_to_upload_user_avatar_wo_data
        )

        assert request.status_code == status.HTTP_400_BAD_REQUEST
        assert request.data["user_avatar_url"][0] == (
            error_resp_data.file_not_submitted
        )

    def test_should_response_large_size_too_large_error(
            self,
            client,
            user_auth_headers,
            data_to_upload_user_avatar_w_big_file
    ):
        request = client.post(
            reverse("user_api:upload_user_avatar"),
            headers=user_auth_headers,
            data=data_to_upload_user_avatar_w_big_file
        )

        assert request.status_code == status.HTTP_413_REQUEST_ENTITY_TOO_LARGE
        assert request.data["detail"] == error_resp_data.file_size_too_large

    def test_should_response_invalid_image_ext_error(
            self,
            client,
            user_auth_headers,
            data_to_upload_user_avatar_w_file_w_invalid_ext
    ):
        request = client.post(
            reverse("user_api:upload_user_avatar"),
            headers=user_auth_headers,
            data=data_to_upload_user_avatar_w_file_w_invalid_ext
        )

        assert request.status_code == status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
        assert request.data["detail"] == error_resp_data.invalid_file_ext
