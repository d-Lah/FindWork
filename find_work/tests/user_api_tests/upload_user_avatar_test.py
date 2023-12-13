import pytest

from django.urls import reverse

from rest_framework import status

from user.models import (
    Profile,
    UserAvatar,
)
from apps.response_error import (
    ResponseInvalidImageExtError,
    ResponseImageSizeTooLargeError,
    ResponseUserAvatarFieldEmptyError,
)
from apps.response_success import ResponseUpload


@pytest.mark.django_db
class TestUploadUserAvatar:
    def test_should_upload_user_avatar(
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
        assert request.status_code == status.HTTP_201_CREATED
        assert request.data.get(
            "status") == ResponseUpload.response_data["status"]

    def test_should_response_auth_headers_error_in_upload_user_avatar(
            self,
            client,
    ):
        request = client.post(
            reverse("user_api:upload_user_avatar"),
        )
        assert request.status_code == status.HTTP_401_UNAUTHORIZED

    def test_should_response_user_avatar_field_empty_error(
            self,
            client,
            user_auth_headers
    ):
        request = client.post(
            reverse("user_api:upload_user_avatar"),
            headers=user_auth_headers,
        )
        assert request.status_code == status.HTTP_400_BAD_REQUEST
        assert request.data.get("error") == (
            ResponseUserAvatarFieldEmptyError.response_data["error"]
        )

    def test_should_response_image_size_too_large_error_in_upload_user_avatar(
            self,
            client,
            user_auth_headers,
            data_to_response_image_size_too_large_error
    ):
        request = client.post(
            reverse("user_api:upload_user_avatar"),
            headers=user_auth_headers,
            data=data_to_response_image_size_too_large_error
        )
        assert request.status_code == status.HTTP_413_REQUEST_ENTITY_TOO_LARGE
        assert request.data.get("error") == (
            ResponseImageSizeTooLargeError.response_data["error"]
        )

    def test_should_response_invalid_image_ext_error(
            self,
            client,
            user_auth_headers,
            data_to_resonse_invalid_image_ext_error
    ):
        request = client.post(
            reverse("user_api:upload_user_avatar"),
            headers=user_auth_headers,
            data=data_to_resonse_invalid_image_ext_error
        )
        assert request.status_code == status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
        assert request.data.get("error") == (
            ResponseInvalidImageExtError.response_data["error"]
        )
