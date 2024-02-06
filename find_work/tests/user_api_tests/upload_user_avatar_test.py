import pytest

from django.urls import reverse

from user.models import (
    Profile,
    UserAvatar,
)

from util.error_resp_data import (
    AuthHeadersError,
    FieldsEmptyError,
    InvalidFileExtError,
    FileSizeTooLargeError,
)
from util.success_resp_data import UploadSuccess


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
        assert request.status_code == UploadSuccess().get_status()
        assert request.data["success"] == (
            UploadSuccess().get_data()["success"]
        )

    def test_should_response_auth_headers_error(
            self,
            client,
    ):
        request = client.post(
            reverse("user_api:upload_user_avatar"),
        )

        assert request.status_code == AuthHeadersError().get_status()
        assert request.data["detail"] == (
            AuthHeadersError().get_data()["detail"]
        )

    def test_should_response_avatar_fields_empty_error(
            self,
            client,
            user_auth_headers
    ):
        request = client.post(
            reverse("user_api:upload_user_avatar"),
            headers=user_auth_headers,
        )
        assert request.status_code == FieldsEmptyError().get_status()
        assert request.data["fields"] == (
            FieldsEmptyError().get_data()["fields"]
        )

    def test_should_response_image_size_too_large_error(
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
        assert request.status_code == FileSizeTooLargeError().get_status()
        assert request.data["file"] == (
            FileSizeTooLargeError().get_data()["file"]
        )

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
        assert request.status_code == InvalidFileExtError().get_status()
        assert request.data["file"] == (
            InvalidFileExtError().get_data()["file"]
        )
