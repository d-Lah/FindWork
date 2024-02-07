import pytest

from django.urls import reverse

from util.error_resp_data import (
    AuthHeadersError,
    CompanyNotFoundError,
)
from util.success_resp_data import GetSuccess


@pytest.mark.django_db
class TestCompanyInfo:
    def test_should_get_resume_info(
            self,
            client,
            get_company_id,
            user_auth_headers,
    ):
        request = client.get(
            reverse(
                "company_api:company_info",
                kwargs=get_company_id
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
            get_company_id
    ):
        request = client.get(
            reverse(
                "company_api:company_info",
                kwargs=get_company_id
            ),
        )

        assert request.status_code == AuthHeadersError().get_status()
        assert request.data["detail"] == (
            AuthHeadersError().get_data()["detail"]
        )

    def test_should_response_resume_not_found(
            self,
            client,
            user_auth_headers,
            get_wrong_company_id
    ):
        request = client.get(
            reverse(
                "company_api:company_info",
                kwargs=get_wrong_company_id
            ),
            headers=user_auth_headers
        )
        assert request.status_code == CompanyNotFoundError().get_status()
        assert request.data["company"] == (
            CompanyNotFoundError().get_data()["company"]
        )
