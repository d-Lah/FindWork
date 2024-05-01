import pytest

from django.urls import reverse

from rest_framework import status

from company.models import Company

from util import error_resp_data
from util import success_resp_data


@pytest.mark.django_db
class TestCreateCompany:
    def test_should_create_company(
            self,
            client,
            create_user,
            user_auth_headers,
            data_to_create_company
    ):
        request = client.post(
            reverse("company_api:create_company"),
            headers=user_auth_headers,
            data=data_to_create_company
        )

        assert request.status_code == success_resp_data.create["status_code"]
        assert request.data["detail"] == (
            success_resp_data.create["data"]["detail"]
        )
        assert Company.objects.filter(pk=1).first()

    def test_should_response_auth_headers_error(
            self,
            client,
    ):
        request = client.post(
            reverse("company_api:create_company"),
        )

        assert request.status_code == status.HTTP_401_UNAUTHORIZED
        assert request.data["detail"] == (
            error_resp_data.auth_headers
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
            reverse("company_api:create_company"),
            headers=user_auth_headers
        )

        assert request.status_code == status.HTTP_403_FORBIDDEN
        assert request.data["detail"] == (
            error_resp_data.user_not_employer
        )

    def test_should_response_fields_empty_error(
            self,
            client,
            user_auth_headers,
            data_to_create_company_wo_data
    ):
        request = client.post(
            reverse("company_api:create_company"),
            headers=user_auth_headers,
            data=data_to_create_company_wo_data
        )

        assert request.status_code == status.HTTP_400_BAD_REQUEST
        assert request.data["name"][0] == (
            error_resp_data.field_is_blank
        )

    def test_should_response_name_already_exists_error(
            self,
            client,
            user_auth_headers,
            data_to_create_company_w_already_exists_name
    ):
        request = client.post(
            reverse("company_api:create_company"),
            headers=user_auth_headers,
            data=data_to_create_company_w_already_exists_name
        )

        assert request.status_code == status.HTTP_400_BAD_REQUEST
        assert request.data["name"][0] == error_resp_data.field_not_unique
