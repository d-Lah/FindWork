import pytest

from django.urls import reverse

from util.error_resp_data import (
    AuthHeadersError,
    ResumeNotFoundError,
)
from util.success_resp_data import GetSuccess


@pytest.mark.django_db
class TestResumeInfo:
    def test_should_get_resume_info(
            self,
            client,
            user_auth_headers,
            data_to_resume_info_w_resume_id
    ):
        request = client.get(
            reverse(
                "resume_api:resume_info",
                kwargs=data_to_resume_info_w_resume_id
            ),
            headers=user_auth_headers
        )
        assert request.status_code == GetSuccess().get_status()
        assert request.data["success"] == (
            GetSuccess().get_data()["success"]
        )

    def test_should_response_auth_headers_error(
            self,
            client,
            data_to_resume_info_w_resume_id
    ):
        request = client.get(
            reverse(
                "resume_api:resume_info",
                kwargs=data_to_resume_info_w_resume_id
            ),
        )
        assert request.status_code == AuthHeadersError().get_status()

    def test_should_response_resume_not_found(
            self,
            client,
            user_auth_headers,
            data_to_resume_info_w_wrong_resume_id
    ):
        request = client.get(
            reverse(
                "resume_api:resume_info",
                kwargs=data_to_resume_info_w_wrong_resume_id
            ),
            headers=user_auth_headers
        )
        assert request.status_code == ResumeNotFoundError().get_status()
        assert request.data["resume"] == (
            ResumeNotFoundError().get_data()["resume"]
        )
