import pytest

from django.urls import reverse

from company.models import Company

from util.error_resp_data import (
    AuthHeadersError,
    CompanyNotFoundError,
    UserNotEmployerError,
)
from util.success_resp_data import DeleteSuccess


@pytest.mark.django_db
class TestDeleteCompany:
    def test_should_delete_resume(
            self,
            client,
            create_company,
            create_user,
            user_auth_headers
    ):
        request = client.delete(
            reverse("company_api:delete_company"),
            headers=user_auth_headers
        )

        assert request.status_code == DeleteSuccess().get_status()
        assert request.data["success"] == DeleteSuccess().get_data()["success"]
        company = Company.objects.filter(pk=1).first()
        assert company.is_delete

    def test_response_user_auth_headers_error(
            self,
            client,
            create_resume,
    ):
        request = client.delete(
            reverse("company_api:delete_company"),
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

        request = client.delete(
            reverse("company_api:delete_company"),
            headers=user_auth_headers
        )

        assert request.status_code == UserNotEmployerError().get_status()
        assert request.data["detail"] == (
            UserNotEmployerError().get_data()["detail"]
        )

    def test_response_company_not_found(
            self,
            client,
            create_resume,
            user_auth_headers,
    ):
        create_resume.is_delete = True
        create_resume.save()

        request = client.delete(
            reverse("company_api:delete_company"),
            headers=user_auth_headers
        )

        assert request.status_code == CompanyNotFoundError().get_status()
        assert request.data["company"] == (
            CompanyNotFoundError().get_data()["company"]
        )
