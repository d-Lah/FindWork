import pytest

from django.urls import reverse

from rest_framework import status

from vacancy.models import Vacancy

from util import error_resp_data
from util import success_resp_data


@pytest.mark.django_db
class TestDeleteVacancy:
    def test_should_delete_resume(
            self,
            client,
            get_vacancy_id,
            user_auth_headers,
    ):
        request = client.delete(
            reverse(
                "vacancy_api:delete_vacancy",
                kwargs=get_vacancy_id
            ),
            headers=user_auth_headers
        )

        assert request.status_code == success_resp_data.delete["status_code"]
        assert request.data["detail"] == (
            success_resp_data.delete["data"]["detail"]
        )
        resume = Vacancy.objects.filter(pk=1).first()
        assert resume.is_delete

    def test_response_user_auth_headers_error(
            self,
            client,
            create_resume,
            get_vacancy_id,
    ):
        request = client.delete(
            reverse(
                "vacancy_api:delete_vacancy",
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
                "vacancy_api:delete_vacancy",
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
                "vacancy_api:delete_vacancy",
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
                "vacancy_api:delete_vacancy",
                kwargs=get_vacancy_id
            ),
            headers=sec_user_auth_headers
        )

        assert request.status_code == status.HTTP_403_FORBIDDEN
        assert request.data["detail"] == (
            error_resp_data.company_not_vacancy_creator
        )
