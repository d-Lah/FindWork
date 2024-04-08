import pytest

from django.urls import reverse

from util.error_resp_data import (
    VacancyNotFound,
    AuthHeadersError,
    FieldsEmptyError,
    SkillNotFoundError,
    UserNotCompanyOwner,
    CompanyNotVacancyCreator,
    SpecializationNotFoundError,
    WorkExperienceNotFoundError,
    TypeOfEmploymentNotFoundError,
)
from util.success_resp_data import UpdateSuccess


@pytest.mark.django_db
class TestEditVacancy:
    def test_should_edit_vacancy(
            self,
            client,
            get_vacancy_id,
            user_auth_headers,
            data_to_edit_vacancy_info
    ):
        request = client.put(
            reverse(
                "vacancy_api:edit_vacancy_info",
                kwargs=get_vacancy_id
            ),
            headers=user_auth_headers,
            data=data_to_edit_vacancy_info
        )
        assert request.status_code == UpdateSuccess().get_status()
        assert request.data["success"] == (
            UpdateSuccess().get_data()["success"]
        )

    def test_should_responce_auth_headers_error(
            self,
            client,
            get_vacancy_id
    ):
        request = client.put(
            reverse(
                "vacancy_api:edit_vacancy_info",
                kwargs=get_vacancy_id
            ),
        )
        assert request.status_code == AuthHeadersError().get_status()
        assert request.data["detail"] == (
            AuthHeadersError().get_data()["detail"]
        )

    def test_should_response_vacancy_not_found_error(
            self,
            client,
            create_company,
            user_auth_headers,
            get_wrong_vacancy_id,
            data_to_edit_vacancy_info
    ):
        request = client.put(
            reverse(
                "vacancy_api:edit_vacancy_info",
                kwargs=get_wrong_vacancy_id
            ),
            headers=user_auth_headers,
            data=data_to_edit_vacancy_info
        )

        assert request.status_code == VacancyNotFound().get_status()
        assert request.data["detail"] == (
            VacancyNotFound().get_data()["vacancy"]
        )

    def test_should_responce_user_not_company_owner(
            self,
            client,
            get_vacancy_id,
            sec_user_auth_headers,
    ):
        request = client.put(
            reverse(
                "vacancy_api:edit_vacancy_info",
                kwargs=get_vacancy_id
            ),
            headers=sec_user_auth_headers
        )

        assert request.status_code == UserNotCompanyOwner().get_status()
        assert request.data["detail"] == (
            UserNotCompanyOwner().get_data()["detail"]
        )

    def test_should_responce_company_not_vacancy_creator(
            self,
            client,
            get_vacancy_id,
            create_sec_company,
            sec_user_auth_headers,
    ):
        request = client.put(
            reverse(
                "vacancy_api:edit_vacancy_info",
                kwargs=get_vacancy_id
            ),
            headers=sec_user_auth_headers
        )

        assert request.status_code == CompanyNotVacancyCreator().get_status()
        assert request.data["detail"] == (
            CompanyNotVacancyCreator().get_data()["detail"]
        )

    def test_should_responce_fields_empty_error(
            self,
            client,
            get_vacancy_id,
            create_company,
            user_auth_headers,
            data_to_edit_vacancy_info_wo_data,
    ):
        request = client.put(
            reverse(
                "vacancy_api:edit_vacancy_info",
                kwargs=get_vacancy_id
            ),
            headers=user_auth_headers,
            data=data_to_edit_vacancy_info_wo_data
        )

        assert request.status_code == FieldsEmptyError().get_status()
        for key in request.data:
            assert (
                FieldsEmptyError.detail["opt1"] in request.data[key][0]
                or FieldsEmptyError.detail["opt2"] in request.data[key][0]
            )

    def test_should_response_wrong_rqd_specialization_error(
            self,
            client,
            get_vacancy_id,
            create_company,
            user_auth_headers,
            data_to_edit_vacancy_w_wrong_rqd_specialization
    ):
        request = client.put(
            reverse(
                "vacancy_api:edit_vacancy_info",
                kwargs=get_vacancy_id
            ),
            headers=user_auth_headers,
            data=data_to_edit_vacancy_w_wrong_rqd_specialization
        )

        assert request.status_code == (
            SpecializationNotFoundError().get_status()
        )
        assert request.data["detail"] == (
            SpecializationNotFoundError().get_data()["specialization"]
        )

    def test_should_response_wrong_rqd_skill_error(
            self,
            client,
            get_vacancy_id,
            create_company,
            user_auth_headers,
            data_to_edit_vacancy_w_wrong_rqd_skill

    ):
        request = client.put(
            reverse(
                "vacancy_api:edit_vacancy_info",
                kwargs=get_vacancy_id
            ),
            headers=user_auth_headers,
            data=data_to_edit_vacancy_w_wrong_rqd_skill
        )

        assert request.status_code == SkillNotFoundError().get_status()
        assert request.data["detail"] == (
            SkillNotFoundError().get_data()["skill"]
        )

    def test_should_response_wrong_rqd_work_experience_error(
            self,
            client,
            get_vacancy_id,
            create_company,
            user_auth_headers,
            data_to_edit_vacancy_w_wrong_rqd_work_experience
    ):
        request = client.put(
            reverse(
                "vacancy_api:edit_vacancy_info",
                kwargs=get_vacancy_id
            ),
            headers=user_auth_headers,
            data=data_to_edit_vacancy_w_wrong_rqd_work_experience
        )

        assert request.status_code == (
            WorkExperienceNotFoundError().get_status()
        )
        assert request.data["detail"] == (
            WorkExperienceNotFoundError().get_data()["work_experience"]
        )

    def test_should_response_wrong_rqd_type_of_employment_error(
            self,
            client,
            get_vacancy_id,
            create_company,
            user_auth_headers,
            data_to_edit_vacancy_w_wrong_rqd_type_of_employment
    ):
        request = client.put(
            reverse(
                "vacancy_api:edit_vacancy_info",
                kwargs=get_vacancy_id
            ),
            headers=user_auth_headers,
            data=data_to_edit_vacancy_w_wrong_rqd_type_of_employment
        )

        assert request.status_code == (
            TypeOfEmploymentNotFoundError().get_status()
        )
        assert request.data["detail"] == (
            TypeOfEmploymentNotFoundError().get_data()["type_of_employment"]
        )
