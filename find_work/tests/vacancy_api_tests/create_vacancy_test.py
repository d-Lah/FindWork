import pytest

from django.urls import reverse

from vacancy.models import Vacancy

from util.error_resp_data import (
    AuthHeadersError,
    FieldsEmptyError,
    SkillNotFoundError,
    UserNotCompanyOwner,
    SpecializationNotFoundError,
    WorkExperienceNotFoundError,
    TypeOfEmploymentNotFoundError,
)
from util.success_resp_data import CreateSuccess


@pytest.mark.django_db
class TestCreateVacancy:
    def test_should_create_vacancy(
            self,
            client,
            create_company,
            user_auth_headers,
            data_to_create_vacancy,
    ):
        request = client.post(
            reverse("vacancy_api:create_vacancy"),
            headers=user_auth_headers,
            data=data_to_create_vacancy
        )

        assert request.status_code == CreateSuccess().get_status()
        assert request.data["success"] == (
            CreateSuccess().get_data()["success"]
        )
        assert Vacancy.objects.filter(pk=1).first()

    def test_should_responce_auth_headers_error(
            self,
            client,
    ):
        request = client.post(
            reverse("vacancy_api:create_vacancy"),
        )

        assert request.status_code == AuthHeadersError().get_status()
        assert request.data["detail"] == (
            AuthHeadersError().get_data()["detail"]
        )

    def test_should_responce_user_not_company_owner(
            self,
            client,
            user_auth_headers
    ):
        request = client.post(
            reverse("vacancy_api:create_vacancy"),
            headers=user_auth_headers
        )

        assert request.status_code == UserNotCompanyOwner().get_status()
        assert request.data["detail"] == (
            UserNotCompanyOwner().get_data()["detail"]
        )

    def test_should_responce_fields_empty_error(
            self,
            client,
            create_company,
            user_auth_headers,
            data_to_create_vacancy_wo_data
    ):
        request = client.post(
            reverse("vacancy_api:create_vacancy"),
            headers=user_auth_headers,
            data=data_to_create_vacancy_wo_data
        )

        assert request.status_code == FieldsEmptyError().get_status()
        assert request.data["fields"] == (
            FieldsEmptyError().get_data()["fields"]
        )

    def test_should_response_wrong_rqd_specialization_error(
            self,
            client,
            create_company,
            user_auth_headers,
            data_to_create_vacancy_w_wrong_rqd_specialization
    ):
        request = client.post(
            reverse("vacancy_api:create_vacancy"),
            headers=user_auth_headers,
            data=data_to_create_vacancy_w_wrong_rqd_specialization
        )

        assert request.status_code == (
            SpecializationNotFoundError().get_status()
        )
        assert request.data["rqd_specialization"] == (
            SpecializationNotFoundError().get_data()["specialization"]
        )

    def test_should_response_wrong_rqd_skill_error(
            self,
            client,
            create_company,
            user_auth_headers,
            data_to_create_vacancy_w_wrong_rqd_skill

    ):
        request = client.post(
            reverse("vacancy_api:create_vacancy"),
            headers=user_auth_headers,
            data=data_to_create_vacancy_w_wrong_rqd_skill
        )

        assert request.status_code == SkillNotFoundError().get_status()
        assert request.data["rqd_skill"] == (
            SkillNotFoundError().get_data()["skill"]
        )

    def test_should_response_wrong_rqd_work_experience_error(
            self,
            client,
            create_company,
            user_auth_headers,
            data_to_create_vacancy_w_wrong_rqd_work_experience
    ):
        request = client.post(
            reverse("vacancy_api:create_vacancy"),
            headers=user_auth_headers,
            data=data_to_create_vacancy_w_wrong_rqd_work_experience
        )

        assert request.status_code == (
            WorkExperienceNotFoundError().get_status()
        )
        assert request.data["rqd_work_experience"] == (
            WorkExperienceNotFoundError().get_data()["work_experience"]
        )

    def test_should_response_wrong_rqd_type_of_employment_error(
            self,
            client,
            create_company,
            user_auth_headers,
            data_to_create_vacancy_w_wrong_rqd_type_of_employment
    ):
        request = client.post(
            reverse("vacancy_api:create_vacancy"),
            headers=user_auth_headers,
            data=data_to_create_vacancy_w_wrong_rqd_type_of_employment
        )

        assert request.status_code == (
            TypeOfEmploymentNotFoundError().get_status()
        )
        assert request.data["rqd_type_of_employment"] == (
            TypeOfEmploymentNotFoundError().get_data()["type_of_employment"]
        )
