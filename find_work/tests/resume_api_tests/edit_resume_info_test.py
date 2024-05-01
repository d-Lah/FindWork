import pytest

from django.urls import reverse

from rest_framework import status

from resume.models import Resume

from util import error_resp_data
from util import success_resp_data


@pytest.mark.django_db
class TestEditResumeInfo:
    def test_should_edit_resume_info(
            self,
            client,
            get_resume_id,
            user_auth_headers,
            data_to_update_resume_info,
    ):
        request = client.put(
            reverse(
                "resume_api:edit_resume_info",
                kwargs=get_resume_id
            ),
            headers=user_auth_headers,
            data=data_to_update_resume_info
        )

        assert request.status_code == status.HTTP_200_OK
        assert request.data["detail"] == (
            success_resp_data.update["data"]["detail"]
        )
        resume = Resume.objects.filter(pk=1).first()
        assert resume.about == data_to_update_resume_info["about"]

    def test_should_response_auth_headers_error(
            self,
            client,
            get_resume_id,
    ):
        request = client.put(
            reverse(
                "resume_api:edit_resume_info",
                kwargs=get_resume_id
            ),
        )

        assert request.status_code == status.HTTP_401_UNAUTHORIZED
        assert request.data["detail"] == error_resp_data.auth_headers

    def test_should_response_resume_not_found(
            self,
            client,
            user_auth_headers,
            get_wrong_resume_id,
    ):

        request = client.put(
            reverse(
                "resume_api:edit_resume_info",
                kwargs=get_wrong_resume_id
            ),
            headers=user_auth_headers,
        )
        assert request.status_code == status.HTTP_404_NOT_FOUND
        assert request.data["detail"] == error_resp_data.resume_not_found

    def test_should_response_user_not_resume_owner_error(
            self,
            client,
            get_resume_id,
            user_auth_headers,
            sec_user_auth_headers
    ):

        request = client.post(
            reverse(
                "resume_api:edit_resume_info",
                kwargs=get_resume_id
            ),
            headers=sec_user_auth_headers
        )

        assert request.status_code == status.HTTP_403_FORBIDDEN
        assert request.data["detail"] == error_resp_data.user_not_resume_owner

    def test_should_response_fields_empty_error(
            self,
            client,
            get_resume_id,
            user_auth_headers,
            data_to_edit_resume_info_wo_data
    ):
        request = client.put(
            reverse(
                "resume_api:edit_resume_info",
                kwargs=get_resume_id
            ),
            headers=user_auth_headers,
            data=data_to_edit_resume_info_wo_data
        )

        assert request.status_code == status.HTTP_400_BAD_REQUEST
        for field in request.data:
            assert (
                request.data[field][0] == error_resp_data.field_is_blank
                or request.data[field][0] == error_resp_data.field_is_required
            )

    def test_should_response_fields_not_exists_error(
            self,
            client,
            get_resume_id,
            user_auth_headers,
            data_to_edit_resume_info_w_not_exists_field
    ):
        request = client.put(
            reverse(
                "resume_api:edit_resume_info",
                kwargs=get_resume_id
            ),
            headers=user_auth_headers,
            data=data_to_edit_resume_info_w_not_exists_field
        )

        assert request.status_code == status.HTTP_400_BAD_REQUEST
        for field in request.data:
            assert (
                request.data[field][0] == error_resp_data.field_not_exists
                or request.data[field][0][0] == error_resp_data.
                field_not_exists
            )
