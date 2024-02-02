import pytest

from django.urls import reverse

from resume.models import Resume

from util.success_resp_data import DeleteSuccess
from util.error_resp_data import (
    AuthHeadersError,
    ResumeNotFoundError,
)


@pytest.mark.django_db
class TestDeleteResume:
    def test_should_delete_resume(
            self,
            client,
            create_resume,
            create_new_user,
            user_auth_headers
    ):
        request = client.delete(
            reverse("resume_api:delete_resume"),
            headers=user_auth_headers
        )

        assert request.status_code == DeleteSuccess().get_status()
        assert request.data["success"] == DeleteSuccess().get_data()["success"]

    def test_response_user_auth_headers_error(
            self,
            client,
            create_resume,
    ):
        request = client.delete(
            reverse("resume_api:delete_resume"),
        )

        assert request.status_code == AuthHeadersError().get_status()

    def test_response_resume_not_found(
            self,
            client,
            create_resume,
            create_new_user,
            user_auth_headers,
    ):
        create_new_user.is_employee = False
        create_new_user.save()

        request = client.delete(
            reverse("resume_api:delete_resume"),
            headers=user_auth_headers
        )

        assert request.status_code == ResumeNotFoundError().get_status()
        assert request.data["resume"] == (
            ResumeNotFoundError().get_data()["resume"]
        )
