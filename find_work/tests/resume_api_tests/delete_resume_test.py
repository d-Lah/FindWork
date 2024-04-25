import pytest

from django.urls import reverse

from rest_framework import status

from resume.models import Resume

from util import error_resp_data
from util import success_resp_data


@pytest.mark.django_db
class TestDeleteResume:
    def test_should_delete_resume(
            self,
            client,
            get_resume_id,
            user_auth_headers,
    ):
        request = client.delete(
            reverse(
                "resume_api:delete_resume",
                kwargs=get_resume_id
            ),
            headers=user_auth_headers
        )

        assert request.status_code == status.HTTP_200_OK
        assert request.data["detail"] == (
            success_resp_data.delete["data"]["detail"]
        )
        resume = Resume.objects.filter(pk=1).first()
        assert resume.is_delete

    def test_response_user_auth_headers_error(
            self,
            client,
            get_resume_id,
    ):
        request = client.delete(
            reverse(
                "resume_api:delete_resume",
                kwargs=get_resume_id
            ),
        )

        assert request.status_code == status.HTTP_401_UNAUTHORIZED
        assert request.data["detail"] == error_resp_data.auth_headers

    def test_response_resume_not_found(
            self,
            client,
            user_auth_headers,
            get_wrong_resume_id,
    ):
        request = client.delete(
            reverse(
                "resume_api:delete_resume",
                kwargs=get_wrong_resume_id
            ),
            headers=user_auth_headers
        )

        assert request.status_code == status.HTTP_404_NOT_FOUND
        assert request.data["detail"] == error_resp_data.resume_not_found

    def test_response_user_not_resume_owner_error(
            self,
            client,
            get_resume_id,
            sec_user_auth_headers,
    ):
        request = client.delete(
            reverse(
                "resume_api:delete_resume",
                kwargs=get_resume_id
            ),
            headers=sec_user_auth_headers
        )

        assert request.status_code == status.HTTP_403_FORBIDDEN
        assert request.data["detail"] == error_resp_data.user_not_resume_owner
