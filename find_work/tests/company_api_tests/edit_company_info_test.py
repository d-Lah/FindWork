import pytest

from django.urls import reverse

from rest_framework import status

from company.models import Company

from util import error_resp_data
from util import success_resp_data


@pytest.mark.django_db
class TestCreateCompany:
    def test_should_create_company(
            self,
            client,
            get_company_id,
            user_auth_headers,
            data_to_edit_company_info
    ):
        request = client.put(
            reverse(
                "company_api:edit_company_info",
                kwargs=get_company_id
            ),
            headers=user_auth_headers,
            data=data_to_edit_company_info
        )

        assert request.status_code == success_resp_data.update["status_code"]
        assert request.data["detail"] == (
            success_resp_data.update["data"]["detail"]
        )
        company = Company.objects.filter(pk=1).first()
        assert company.name == data_to_edit_company_info["name"]

    def test_should_response_auth_headers_error(
            self,
            client,
            get_company_id
    ):
        request = client.put(
            reverse(
                "company_api:edit_company_info",
                kwargs=get_company_id
            ),
        )

        assert request.status_code == status.HTTP_401_UNAUTHORIZED
        assert request.data["detail"] == (
            error_resp_data.auth_headers
        )

    def test_should_response_user_not_company_owner_error(
            self,
            client,
            get_company_id,
            sec_user_auth_headers,
    ):

        request = client.put(
            reverse(
                "company_api:edit_company_info",
                kwargs=get_company_id
            ),
            headers=sec_user_auth_headers
        )

        assert request.status_code == status.HTTP_403_FORBIDDEN
        assert request.data["detail"] == (
            error_resp_data.user_not_company_owner
        )

    def test_should_response_fields_empty_error(
            self,
            client,
            get_company_id,
            user_auth_headers,
            data_to_edit_company_info_wo_data
    ):
        request = client.put(
            reverse(
                "company_api:edit_company_info",
                kwargs=get_company_id
            ),
            headers=user_auth_headers,
            data=data_to_edit_company_info_wo_data
        )

        assert request.status_code == status.HTTP_400_BAD_REQUEST
        assert request.data["name"][0] == (
            error_resp_data.field_is_blank
        )

    def test_should_response_name_already_exists_error(
            self,
            client,
            get_company_id,
            user_auth_headers,
            data_to_edit_company_info_w_already_exists_name
    ):
        request = client.put(
            reverse(
                "company_api:edit_company_info",
                kwargs=get_company_id
            ),
            headers=user_auth_headers,
            data=data_to_edit_company_info_w_already_exists_name
        )

        assert request.status_code == status.HTTP_400_BAD_REQUEST
        assert request.data["name"][0] == (
            error_resp_data.field_not_unique
        )

    def test_should_response_company_not_found(
            self,
            client,
            user_auth_headers,
            get_wrong_company_id,
    ):
        request = client.put(
            reverse(
                "company_api:edit_company_info",
                kwargs=get_wrong_company_id
            ),
            headers=user_auth_headers,
        )
        assert request.status_code == status.HTTP_404_NOT_FOUND
        assert request.data["detail"] == (
            error_resp_data.company_not_found
        )
