import pytest

from django.urls import reverse

from company.models import (
    Company,
    CompanyAvatar,
)

from util.error_resp_data import (
    AuthHeadersError,
    FieldsEmptyError,
    InvalidFileExtError,
    FileSizeTooLargeError,
)
from util.success_resp_data import UploadSuccess


@pytest.mark.django_db
class TestUploadCompanyAvatar:
    def test_should_upload_avatar(
            self,
            client,
            mocker,
            create_company,
            user_auth_headers,
            data_to_upload_company_avatar
    ):
        mocker.patch.object(
            Company,
            "save",
            return_value="return ResponseUpload().get_response()")
        mocker.patch.object(
            CompanyAvatar,
            "save",
            return_value="return ResponseUpload().get_response()"
        )

        request = client.post(
            reverse("company_api:upload_company_avatar"),
            headers=user_auth_headers,
            data=data_to_upload_company_avatar
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
            reverse("company_api:upload_company_avatar"),
        )

        assert request.status_code == AuthHeadersError().get_status()
        assert request.data["detail"] == (
            AuthHeadersError().get_data()["detail"]
        )

    def test_should_response_user_not_employer_error(
            self,
            client,
            create_user,
            user_auth_headers,
    ):
        create_user.is_employer = False
        create_user.save()

        request = client.post(
            reverse("company_api:upload_company_avatar"),
        )

        assert request.status_code == AuthHeadersError().get_status()
        assert request.data["detail"] == (
            AuthHeadersError().get_data()["detail"]
        )

    def test_should_response_fields_empty_error(
            self,
            client,
            create_company,
            user_auth_headers,
    ):
        request = client.post(
            reverse("company_api:upload_company_avatar"),
            headers=user_auth_headers,
        )

        assert request.status_code == FieldsEmptyError().get_status()
        assert request.data["fields"] == (
            FieldsEmptyError().get_data()["fields"]
        )

    def test_should_response_image_size_too_large_error(
            self,
            client,
            create_company,
            user_auth_headers,
            data_to_upload_company_avatar_w_big_file
    ):
        request = client.post(
            reverse("company_api:upload_company_avatar"),
            headers=user_auth_headers,
            data=data_to_upload_company_avatar_w_big_file
        )

        assert request.status_code == FileSizeTooLargeError().get_status()
        assert request.data["file"] == (
            FileSizeTooLargeError().get_data()["file"]
        )

    def test_should_response_invalid_image_ext_error(
            self,
            client,
            create_company,
            user_auth_headers,
            data_to_upload_company_avatar_w_file_w_invalid_ext
    ):
        request = client.post(
            reverse("company_api:upload_company_avatar"),
            headers=user_auth_headers,
            data=data_to_upload_company_avatar_w_file_w_invalid_ext
        )

        assert request.status_code == InvalidFileExtError().get_status()
        assert request.data["file"] == (
            InvalidFileExtError().get_data()["file"]
        )
