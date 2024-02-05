import pytest

from django.urls import reverse

from resume.models import Resume

from util.error_resp_data import (
    AuthHeadersError,
    FieldsEmptyError,
    FieldsNotFoundError,
    ResumeNotFoundError,
    UserNotEmployeeError,
)
from util.success_resp_data import (
    UpdateSuccess
)


@pytest.mark.django_db
class TestEditResumeInfo:
    def test_should_edit_resume_info(
            self,
            client,
            create_resume,
            user_auth_headers,
            data_to_update_resume_info,
    ):
        request = client.put(
            reverse("resume_api:edit_resume_info"),
            headers=user_auth_headers,
            data=data_to_update_resume_info
        )

        assert request.status_code == UpdateSuccess().get_status()
        assert request.data["success"] == (
            UpdateSuccess().get_data()["success"]
        )
        resume = Resume.objects.filter(pk=1).first()
        assert resume.about == data_to_update_resume_info["about"]

    def test_should_response_auth_headers_error(
            self,
            client,
    ):
        request = client.put(
            reverse("resume_api:edit_resume_info"),
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
            reverse("resume_api:edit_resume_info"),
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
            data_to_edit_resume_info_wo_data
    ):
        request = client.put(
            reverse("resume_api:edit_resume_info"),
            headers=user_auth_headers,
            data=data_to_edit_resume_info_wo_data
        )

        assert request.status_code == FieldsEmptyError().get_status()
        assert request.data["fields"] == (
            FieldsEmptyError().get_data()["fields"]
        )

    def test_should_response_resume_not_found(
            self,
            client,
            create_resume,
            user_auth_headers,
    ):
        create_resume.is_delete = True
        create_resume.save()

        request = client.put(
            reverse("resume_api:edit_resume_info"),
            headers=user_auth_headers,
        )
        assert request.status_code == ResumeNotFoundError().get_status()
        assert request.data["resume"] == (
            ResumeNotFoundError().get_data()["resume"]
        )

    def test_should_response_wrong_specialization_error(
            self,
            client,
            user_auth_headers,
            data_to_edit_resume_info_w_wrong_specialization
    ):
        request = client.put(
            reverse("resume_api:edit_resume_info"),
            headers=user_auth_headers,
            data=data_to_edit_resume_info_w_wrong_specialization
        )

        assert request.status_code == FieldsNotFoundError().get_status()
        assert request.data["specialization"] == (
            FieldsNotFoundError().get_data()["specialization"]
        )

    def test_should_response_wrong_skill_error(
            self,
            client,
            user_auth_headers,
            data_to_edit_resume_info_w_wrong_skill
    ):
        request = client.put(
            reverse("resume_api:edit_resume_info"),
            headers=user_auth_headers,
            data=data_to_edit_resume_info_w_wrong_skill
        )

        assert request.status_code == FieldsNotFoundError().get_status()
        assert request.data["skill"] == (
            FieldsNotFoundError().get_data()["skill"]
        )

    def test_should_response_wrong_work_experience_error(
            self,
            client,
            user_auth_headers,
            data_to_edit_resume_info_w_wrong_work_experience
    ):
        request = client.put(
            reverse("resume_api:edit_resume_info"),
            headers=user_auth_headers,
            data=data_to_edit_resume_info_w_wrong_work_experience
        )

        assert request.status_code == FieldsNotFoundError().get_status()
        assert request.data["work_experience"] == (
            FieldsNotFoundError().get_data()["work_experience"]
        )

    def test_should_response_wrong_type_of_employment_error(
            self,
            client,
            user_auth_headers,
            data_to_edit_resume_info_w_wrong_type_of_employment
    ):
        request = client.put(
            reverse("resume_api:edit_resume_info"),
            headers=user_auth_headers,
            data=data_to_edit_resume_info_w_wrong_type_of_employment
        )

        assert request.status_code == FieldsNotFoundError().get_status()
        assert request.data["type_of_employment"] == (
            FieldsNotFoundError().get_data()["type_of_employment"]
        )
