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

    def test_should_response_fields_not_exists_error(
            self,
            client,
            user_auth_headers,
            data_to_create_resume_w_not_exists_fields
    ):
        request = client.post(
            reverse(
                "resume_api:create_resume",
            ),
            headers=user_auth_headers,
            data=data_to_create_resume_w_not_exists_fields
        )

        assert request.status_code == status.HTTP_400_BAD_REQUEST
        for field in request.data:
            assert (
                request.data[field][0] == error_resp_data.field_not_exists
                or request.data[field][0][0] == error_resp_data.
                field_not_exists
            )
