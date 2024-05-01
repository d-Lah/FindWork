import pytest

from django.urls import reverse

from rest_framework import status

from vacancy.models import Vacancy

from util import error_resp_data
from util import success_resp_data


@pytest.mark.django_db
class TestCreateVacancy:
    def test_should_create_vacancy(
            self,
            client,
            get_company_id,
            user_auth_headers,
            data_to_create_vacancy,
    ):
        request = client.post(
            reverse(
                "vacancy_api:create_vacancy",
                kwargs=get_company_id
            ),
            headers=user_auth_headers,
            data=data_to_create_vacancy
        )

        assert request.status_code == success_resp_data.create["status_code"]
        assert request.data["detail"] == (
            success_resp_data.create["data"]["detail"]
        )
        assert Vacancy.objects.filter(pk=1).first()

    def test_should_responce_auth_headers_error(
            self,
            client,
            get_company_id,
    ):
        request = client.post(
            reverse(
                "vacancy_api:create_vacancy",
                kwargs=get_company_id
            ),
        )

        assert request.status_code == status.HTTP_401_UNAUTHORIZED
        assert request.data["detail"] == (
            error_resp_data.auth_headers
        )

    def test_response_company_not_found(
            self,
            client,
            user_auth_headers,
            get_wrong_company_id,
    ):
        request = client.delete(
            reverse(
                "vacancy_api:create_vacancy",
                kwargs=get_wrong_company_id
            ),
            headers=user_auth_headers
        )

        assert request.status_code == status.HTTP_404_NOT_FOUND
        assert request.data["detail"] == error_resp_data.company_not_found

    def test_should_responce_user_not_company_owner(
            self,
            client,
            get_company_id,
            sec_user_auth_headers
    ):
        request = client.post(
            reverse(
                "vacancy_api:create_vacancy",
                kwargs=get_company_id
            ),
            headers=sec_user_auth_headers
        )

        assert request.status_code == status.HTTP_403_FORBIDDEN
        assert request.data["detail"] == (
            error_resp_data.user_not_company_owner
        )

    def test_should_responce_fields_empty_error(
            self,
            client,
            get_company_id,
            user_auth_headers,
            data_to_create_vacancy_wo_data
    ):
        request = client.post(
            reverse(
                "vacancy_api:create_vacancy",
                kwargs=get_company_id
            ),
            headers=user_auth_headers,
            data=data_to_create_vacancy_wo_data
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
            get_company_id,
            user_auth_headers,
            data_to_create_vacancy_w_not_exists_fields
    ):
        request = client.post(
            reverse(
                "vacancy_api:create_vacancy",
                kwargs=get_company_id
            ),
            headers=user_auth_headers,
            data=data_to_create_vacancy_w_not_exists_fields
        )

        assert request.status_code == status.HTTP_400_BAD_REQUEST
        for field in request.data:
            assert (
                request.data[field][0] == error_resp_data.field_not_exists
                or request.data[field][0][0] == error_resp_data.
                field_not_exists
            )
