import pytest

from django.urls import reverse

from company.models import Company

from util.error_resp_data import (
    AuthHeadersError,
    FieldsEmptyError,
    UserNotEmployerError,
    NameAlreadyExistsError,
)

from util.success_resp_data import CreateSuccess


@pytest.mark.django_db
class TestCreateCompany:
    def test_should_create_company(
            self,
            client,
            create_new_user,
            user_auth_headers,
            data_to_create_company
    ):
        request = client.post(
            reverse("company_api:create_company"),
            headers=user_auth_headers,
            data=data_to_create_company
        )

        assert request.status_code == CreateSuccess().get_status()
        assert request.data == CreateSuccess().get_data()
        assert Company.objects.filter(pk=1).first()

    def test_should_response_auth_headers_error(
            self,
            client,
    ):
        request = client.post(
            reverse("company_api:create_company"),
        )

        assert request.status_code == AuthHeadersError().get_status()
        assert request.data["detail"] == (
            AuthHeadersError().get_data()["detail"]
        )

    def test_should_response_user_not_employer_error(
            self,
            client,
            create_new_user,
            user_auth_headers,
    ):
        create_new_user.is_employer = False
        create_new_user.save()

        request = client.post(
            reverse("company_api:create_company"),
            headers=user_auth_headers
        )

        assert request.status_code == UserNotEmployerError().get_status()
        assert request.data["detail"] == (
            UserNotEmployerError().get_data()["detail"]
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

        assert request.status_code == FieldsEmptyError().get_status()
        assert request.data["fields"] == (
            FieldsEmptyError().get_data()["fields"]
        )
