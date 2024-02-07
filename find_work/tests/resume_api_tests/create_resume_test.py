import pytest

from django.urls import reverse

from resume.models import Resume

from util.error_resp_data import (
    AuthHeadersError,
    FieldsEmptyError,
    SkillNotFoundError,
    UserNotEmployeeError,
    SpecializationNotFoundError,
    WorkExperienceNotFoundError,
    TypeOfEmploymentNotFoundError,
)
from util.success_resp_data import (
    CreateSuccess
)


@pytest.mark.django_db
class TestCreateResume:
    def test_should_create_resume(
            self,
            client,
            create_new_user,
            user_auth_headers,
            data_to_create_resume
    ):
        request = client.post(
            reverse("resume_api:create_resume"),
            headers=user_auth_headers,
            data=data_to_create_resume
        )

        assert request.status_code == CreateSuccess().get_status()
        assert request.data["success"] == CreateSuccess().get_data()["success"]
        assert Resume.objects.filter(pk=1).first()

    def test_should_response_auth_headers_error(
            self,
            client,
    ):
        request = client.put(
            reverse("resume_api:create_resume"),
        )

        assert request.status_code == AuthHeadersError().get_status()
        assert request.data["detail"] == (
            AuthHeadersError().get_data()["detail"]
        )

    def test_should_response_user_not_employee_error(
            self,
            client,
            create_new_user,
            user_auth_headers,
    ):
        create_new_user.is_employee = False
        create_new_user.save()

        request = client.post(
            reverse("resume_api:create_resume"),
            headers=user_auth_headers
        )

        assert request.status_code == UserNotEmployeeError().get_status()
        assert request.data["detail"] == (
            UserNotEmployeeError().get_data()["detail"]
        )

    def test_should_response_fields_empty_error(
            self,
            client,
            user_auth_headers,
            data_to_create_resume_wo_data
    ):
        request = client.post(
            reverse("resume_api:create_resume"),
            headers=user_auth_headers,
            data=data_to_create_resume_wo_data
        )

        assert request.status_code == FieldsEmptyError().get_status()
        assert request.data["fields"] == (
            FieldsEmptyError().get_data()["fields"]
        )

    def test_should_response_wrong_specialization_error(
            self,
            client,
            user_auth_headers,
            data_to_create_resume_w_wrong_specialization
    ):
        request = client.post(
            reverse("resume_api:create_resume"),
            headers=user_auth_headers,
            data=data_to_create_resume_w_wrong_specialization
        )

        assert request.status_code == (
            SpecializationNotFoundError().get_status()
        )
        assert request.data["specialization"] == (
            SpecializationNotFoundError().get_data()["specialization"]
        )

    def test_should_response_wrong_skill_error(
            self,
            client,
            user_auth_headers,
            data_to_create_resume_w_wrong_skill
    ):
        request = client.post(
            reverse("resume_api:create_resume"),
            headers=user_auth_headers,
            data=data_to_create_resume_w_wrong_skill
        )

        assert request.status_code == SkillNotFoundError().get_status()
        assert request.data["skill"] == (
            SkillNotFoundError().get_data()["skill"]
        )

    def test_should_response_wrong_work_experience_error(
            self,
            client,
            user_auth_headers,
            data_to_create_resume_w_wrong_work_experience
    ):
        request = client.post(
            reverse("resume_api:create_resume"),
            headers=user_auth_headers,
            data=data_to_create_resume_w_wrong_work_experience
        )

        assert request.status_code == (
            WorkExperienceNotFoundError().get_status()
        )
        assert request.data["work_experience"] == (
            WorkExperienceNotFoundError().get_data()["work_experience"]
        )

    def test_should_response_wrong_type_of_employment_error(
            self,
            client,
            user_auth_headers,
            data_to_create_resume_w_wrong_type_of_employment
    ):
        request = client.post(
            reverse("resume_api:create_resume"),
            headers=user_auth_headers,
            data=data_to_create_resume_w_wrong_type_of_employment
        )

        assert request.status_code == (
            TypeOfEmploymentNotFoundError().get_status()
        )
        assert request.data["type_of_employment"] == (
            TypeOfEmploymentNotFoundError().get_data()["type_of_employment"]
        )
