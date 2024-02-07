import pytest

from django.urls import reverse

from company.models import Company

from util.error_resp_data import (
    AuthHeadersError,
    FieldsEmptyError,
    UserNotEmployerError,
    CompanyNotFoundError,
    NameAlreadyExistsError,
)

from util.success_resp_data import UpdateSuccess


@pytest.mark.django_db
class TestCreateCompany:
    def test_should_create_company(
            self,
            client,
            create_company,
            create_new_user,
            user_auth_headers,
            data_to_edit_company_info
    ):
        request = client.put(
            reverse("company_api:edit_company_info"),
            headers=user_auth_headers,
            data=data_to_edit_company_info
        )

        assert request.status_code == UpdateSuccess().get_status()
        assert request.data["success"] == (
            UpdateSuccess().get_data()["success"]
        )
        company = Company.objects.filter(pk=1).first()
        assert company.name == data_to_edit_company_info["name"]

    def test_should_response_auth_headers_error(
            self,
            client,
    ):
        request = client.put(
            reverse("company_api:edit_company_info"),
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

        request = client.put(
            reverse("company_api:edit_company_info"),
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
            data_to_edit_company_info_wo_data
    ):
        request = client.put(
            reverse("company_api:edit_company_info"),
            headers=user_auth_headers,
            data=data_to_edit_company_info_wo_data
        )

        assert request.status_code == FieldsEmptyError().get_status()
        assert request.data["fields"] == (
            FieldsEmptyError().get_data()["fields"]
        )

    def test_should_response_name_already_exists_error(
            self,
            client,
            user_auth_headers,
            data_to_edit_company_info_w_already_exists_name
    ):
        request = client.put(
            reverse("company_api:edit_company_info"),
            headers=user_auth_headers,
            data=data_to_edit_company_info_w_already_exists_name
        )

        assert request.status_code == NameAlreadyExistsError().get_status()
        assert request.data["name"] == (
            NameAlreadyExistsError().get_data()["name"]
        )

    def test_should_response_company_not_found(
            self,
            client,
            create_company,
            user_auth_headers,
    ):
        create_company.is_delete = True
        create_company.save()

        request = client.put(
            reverse("company_api:edit_company_info"),
            headers=user_auth_headers,
        )
        assert request.status_code == CompanyNotFoundError().get_status()
        assert request.data["company"] == (
            CompanyNotFoundError().get_data()["company"]
        )
