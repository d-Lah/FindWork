import pytest

from django.urls import reverse

from rest_framework import status

from util.user_api_resp.edit_employee_profile_specialization_resp import (
    EditEmployeeProfileSpecializationResp
)


@pytest.mark.django_db
class TestEditEmployeeProfileSpecialization:
    def test_should_edit_employee_profile_specialization(
            self,
            client,
            user_auth_headers,
            data_to_edit_employee_profile_specialization
    ):
        request = client.put(
            reverse("user_api:edit_employee_profile_specialization"),
            headers=user_auth_headers,
            data=data_to_edit_employee_profile_specialization
        )
        assert request.status_code == status.HTTP_200_OK
        assert request.data["success"] == (
            EditEmployeeProfileSpecializationResp.
            resp_data["successes"][0]["success"]
        )

    def test_should_response_auth_headers_error(
            self,
            client,
    ):
        request = client.put(
            reverse("user_api:edit_profile_info"),
        )
        assert request.status_code == status.HTTP_401_UNAUTHORIZED

    def test_should_response_fields_empty_error(
            self,
            client,
            user_auth_headers,
            data_to_edit_employee_profile_specialization_wo_data
    ):
        request = client.put(
            reverse("user_api:edit_employee_profile_specialization"),
            headers=user_auth_headers,
            data=data_to_edit_employee_profile_specialization_wo_data
        )
        assert request.status_code == status.HTTP_400_BAD_REQUEST
        assert request.data["error"] == (
            EditEmployeeProfileSpecializationResp.
            resp_data["errors"][0]["error"]
        )

    def test_should_response_specialization_not_found_error(
            self,
            client,
            user_auth_headers,
            data_to_edit_employee_profile_specialization_w_wrong_specialization
    ):
        data = (
            data_to_edit_employee_profile_specialization_w_wrong_specialization
        )
        request = client.put(
            reverse("user_api:edit_employee_profile_specialization"),
            headers=user_auth_headers,
            data=data
        )
        assert request.status_code == status.HTTP_404_NOT_FOUND
        assert request.data["error"] == (
            EditEmployeeProfileSpecializationResp.
            resp_data["errors"][1]["error"]
        )
