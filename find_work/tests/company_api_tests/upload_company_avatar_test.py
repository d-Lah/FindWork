import pytest

from django.urls import reverse

from rest_framework import status

from company.models import (
    Company,
    CompanyAvatar,
)

from util import error_resp_data
from util import success_resp_data


@pytest.mark.django_db
class TestUploadCompanyAvatar:
    def test_should_upload_avatar(
            self,
            client,
            mocker,
            get_company_id,
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
            reverse(
                "company_api:upload_company_avatar",
                kwargs=get_company_id
            ),
            headers=user_auth_headers,
            data=data_to_upload_company_avatar
        )
        assert request.status_code == success_resp_data.upload["status_code"]
        assert request.data["detail"] == (
            success_resp_data.upload["data"]["detail"]
        )

    def test_should_response_auth_headers_error(
            self,
            client,
            get_company_id,
    ):
        request = client.post(
            reverse(
                "company_api:upload_company_avatar",
                kwargs=get_company_id
            ),
        )

        assert request.status_code == status.HTTP_401_UNAUTHORIZED
        assert request.data["detail"] == (
            error_resp_data.auth_headers
        )

    def test_should_response_user_not_company_owner_error(
            self,
            client,
            get_company_id,
            sec_user_auth_headers,
    ):
        request = client.post(
            reverse(
                "company_api:upload_company_avatar",
                kwargs=get_company_id
            ),
            headers=sec_user_auth_headers
        )

        assert request.status_code == status.HTTP_403_FORBIDDEN
        assert request.data["detail"] == (
            error_resp_data.user_not_company_owner
        )

    def test_should_response_fields_empty_error(
            self,
            client,
            get_company_id,
            user_auth_headers,
    ):
        request = client.post(
            reverse(
                "company_api:upload_company_avatar",
                kwargs=get_company_id
            ),
            headers=user_auth_headers,
        )

        assert request.status_code == status.HTTP_400_BAD_REQUEST
        assert request.data["company_avatar_url"][0] == (
            error_resp_data.file_not_submitted
        )

    def test_should_response_image_size_too_large_error(
            self,
            client,
            create_company,
            get_company_id,
            user_auth_headers,
            data_to_upload_company_avatar_w_big_file
    ):
        request = client.post(
            reverse(
                "company_api:upload_company_avatar",
                kwargs=get_company_id
            ),
            headers=user_auth_headers,
            data=data_to_upload_company_avatar_w_big_file
        )

        assert request.status_code == status.HTTP_413_REQUEST_ENTITY_TOO_LARGE
        assert request.data["detail"] == (
            error_resp_data.file_size_too_large
        )

    def test_should_response_invalid_image_ext_error(
            self,
            client,
            create_company,
            get_company_id,
            user_auth_headers,
            data_to_upload_company_avatar_w_file_w_invalid_ext
    ):
        request = client.post(
            reverse(
                "company_api:upload_company_avatar",
                kwargs=get_company_id
            ),
            headers=user_auth_headers,
            data=data_to_upload_company_avatar_w_file_w_invalid_ext
        )

        assert request.status_code == status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
        assert request.data["detail"] == (
            error_resp_data.invalid_file_ext
        )

    def test_should_response_company_not_found_error(
            self,
            client,
            user_auth_headers,
            get_wrong_company_id
    ):
        request = client.post(
            reverse(
                "company_api:upload_company_avatar",
                kwargs=get_wrong_company_id
            ),
            headers=user_auth_headers
        )

        assert request.status_code == status.HTTP_404_NOT_FOUND
        assert request.data["detail"] == (
            error_resp_data.company_not_found
        )
