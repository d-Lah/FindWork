import pytest

from django.urls import reverse

from rest_framework import status

from util import error_resp_data
from util import success_resp_data


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
        assert request.status_code == success_resp_data.update["status_code"]
        assert request.data["detail"] == (
            success_resp_data.update["data"]["detail"]
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
        assert request.status_code == status.HTTP_401_UNAUTHORIZED
        assert request.data["detail"] == (
            error_resp_data.auth_headers
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

        assert request.status_code == status.HTTP_404_NOT_FOUND
        assert request.data["detail"] == (
            error_resp_data.vacancy_not_found
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

        assert request.status_code == status.HTTP_403_FORBIDDEN
        assert request.data["detail"] == (
            error_resp_data.user_not_company_owner
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

        assert request.status_code == status.HTTP_403_FORBIDDEN
        assert request.data["detail"] == (
            error_resp_data.company_not_vacancy_creator
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

        assert request.status_code == status.HTTP_400_BAD_REQUEST
        for field in request.data:
            assert (
                request.data[field][0] == error_resp_data.field_is_blank
                or request.data[field][0] == error_resp_data.field_is_required
            )

    def test_should_response_fields_not_exists_error(
            self,
            client,
            get_vacancy_id,
            create_company,
            user_auth_headers,
            data_to_edit_vacancy_info_w_not_exists_fields
    ):
        request = client.put(
            reverse(
                "vacancy_api:edit_vacancy_info",
                kwargs=get_vacancy_id
            ),
            headers=user_auth_headers,
            data=data_to_edit_vacancy_info_w_not_exists_fields
        )

        assert request.status_code == status.HTTP_400_BAD_REQUEST
        for field in request.data:
            assert (
                request.data[field][0] == error_resp_data.field_not_exists
                or request.data[field][0][0] == error_resp_data.
                field_not_exists
            )
