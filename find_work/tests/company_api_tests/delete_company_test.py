import pytest

from django.urls import reverse

from rest_framework import status

from company.models import Company

from util import error_resp_data
from util import success_resp_data


@pytest.mark.django_db
class TestDeleteResume:
    def test_should_delete_company(
            self,
            client,
            get_company_id,
            user_auth_headers,
    ):
        request = client.delete(
            reverse(
                "company_api:delete_company",
                kwargs=get_company_id
            ),
            headers=user_auth_headers
        )

        assert request.status_code == status.HTTP_200_OK
        assert request.data["detail"] == (
            success_resp_data.delete["data"]["detail"]
        )
        company = Company.objects.filter(pk=1).first()
        assert company.is_delete

    def test_response_user_auth_headers_error(
            self,
            client,
            get_company_id,
    ):
        request = client.delete(
            reverse(
                "company_api:delete_company",
                kwargs=get_company_id
            ),
        )

        assert request.status_code == status.HTTP_401_UNAUTHORIZED
        assert request.data["detail"] == error_resp_data.auth_headers

    def test_response_company_not_found(
            self,
            client,
            user_auth_headers,
            get_wrong_company_id,
    ):
        request = client.delete(
            reverse(
                "company_api:delete_company",
                kwargs=get_wrong_company_id
            ),
            headers=user_auth_headers
        )

        assert request.status_code == status.HTTP_404_NOT_FOUND
        assert request.data["detail"] == error_resp_data.company_not_found

    def test_response_user_not_company_owner_error(
            self,
            client,
            get_company_id,
            sec_user_auth_headers,
    ):
        request = client.delete(
            reverse(
                "company_api:delete_company",
                kwargs=get_company_id
            ),
            headers=sec_user_auth_headers
        )

        assert request.status_code == status.HTTP_403_FORBIDDEN
        assert request.data["detail"] == error_resp_data.user_not_company_owner
