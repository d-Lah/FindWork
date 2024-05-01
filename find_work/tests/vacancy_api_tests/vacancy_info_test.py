import pytest

from django.urls import reverse

from rest_framework import status

from util import error_resp_data
from util import success_resp_data


@pytest.mark.django_db
class TestVacancyInfo:
    def test_should_get_vacancy_info(
        self,
        client,
        get_vacancy_id,
        user_auth_headers,
    ):
        request = client.get(
            reverse(
                "vacancy_api:vacancy_info",
                kwargs=get_vacancy_id
            ),
            headers=user_auth_headers
        )
        assert request.status_code == success_resp_data.get["status_code"]
        assert request.data["detail"] == (
            success_resp_data.get["data"]["detail"]
        )

    def test_should_response_auth_headers_error(
            self,
            client,
            get_vacancy_id
    ):
        request = client.get(
            reverse(
                "vacancy_api:vacancy_info",
                kwargs=get_vacancy_id
            ),
        )

        assert request.status_code == status.HTTP_401_UNAUTHORIZED
        assert request.data["detail"] == (
            error_resp_data.auth_headers
        )

    def test_should_response_vacancy_not_found(
            self,
            client,
            user_auth_headers,
            get_wrong_vacancy_id
    ):
        request = client.get(
            reverse(
                "vacancy_api:vacancy_info",
                kwargs=get_wrong_vacancy_id
            ),
            headers=user_auth_headers
        )
        assert request.status_code == status.HTTP_404_NOT_FOUND
        assert request.data["detail"] == (
            error_resp_data.vacancy_not_found
        )
