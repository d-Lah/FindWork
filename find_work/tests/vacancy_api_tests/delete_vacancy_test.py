import pytest

from django.urls import reverse

from vacancy.models import Vacancy

from util.error_resp_data import (
    VacancyNotFound,
    AuthHeadersError,
    UserNotCompanyOwner,
    CompanyNotVacancyCreator,
)
from util.success_resp_data import DeleteSuccess


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

        assert request.status_code == DeleteSuccess().get_status()
        assert request.data["success"] == DeleteSuccess().get_data()["success"]
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

        assert request.status_code == AuthHeadersError().get_status()
        assert request.data["detail"] == (
            AuthHeadersError().get_data()["detail"]
        )

    def test_should_responce_auth_headers_error(
            self,
            client,
            get_vacancy_id
    ):
        request = client.put(
            reverse(
                "vacancy_api:delete_vacancy",
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
                "vacancy_api:delete_vacancy",
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
                "vacancy_api:delete_vacancy",
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
                "vacancy_api:delete_vacancy",
                kwargs=get_vacancy_id
            ),
            headers=sec_user_auth_headers
        )

        assert request.status_code == CompanyNotVacancyCreator().get_status()
        assert request.data["detail"] == (
            CompanyNotVacancyCreator().get_data()["detail"]
        )
