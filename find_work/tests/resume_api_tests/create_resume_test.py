import pytest

from django.urls import reverse

from rest_framework import status

from resume.models import Resume

from util import error_resp_data
from util import success_resp_data


@pytest.mark.django_db
class TestCreateResume:
    def test_should_create_resume(
            self,
            client,
            create_user,
            user_auth_headers,
            data_to_create_resume
    ):
        request = client.post(
            reverse("resume_api:create_resume"),
            headers=user_auth_headers,
            data=data_to_create_resume
        )

        assert request.status_code == status.HTTP_201_CREATED
        assert request.data["detail"] == (
            success_resp_data.create["data"]["detail"]
        )
        assert Resume.objects.filter(pk=1).first()

    def test_should_response_auth_headers_error(
            self,
            client,
    ):
        request = client.put(
            reverse("resume_api:create_resume"),
        )

        assert request.status_code == status.HTTP_401_UNAUTHORIZED
        assert request.data["detail"] == (
            error_resp_data.auth_headers
        )

    def test_should_response_user_not_employee_error(
            self,
            client,
            create_user,
            user_auth_headers,
    ):
        create_user.is_employee = False
        create_user.save()

        request = client.post(
            reverse("resume_api:create_resume"),
            headers=user_auth_headers
        )

        assert request.status_code == status.HTTP_403_FORBIDDEN
        assert request.data["detail"] == (
            error_resp_data.user_not_employee
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

        assert request.status_code == status.HTTP_400_BAD_REQUEST
        for field in request.data:
            assert (
                request.data[field][0] == error_resp_data.field_is_blank
                or request.data[field][0] == error_resp_data.field_is_required
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

        assert request.status_code == status.HTTP_404_NOT_FOUND
        assert request.data["detail"] == (
            error_resp_data.specialization_not_found
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

        assert request.status_code == status.HTTP_404_NOT_FOUND
        assert request.data["detail"] == (
            error_resp_data.skill_not_found
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

        assert request.status_code == status.HTTP_404_NOT_FOUND
        assert request.data["detail"] == (
            error_resp_data.work_experience_not_found
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

        assert request.status_code == status.HTTP_404_NOT_FOUND
        assert request.data["detail"] == (
            error_resp_data.type_of_employment_not_found
        )
