import pytest

from django.urls import reverse

from rest_framework import status

from util import error_resp_data
from util import success_resp_data


@pytest.mark.django_db
class TestUpdateEmail:
    def test_should_update_email(
            self,
            client,
            user_auth_headers,
            data_to_update_email
    ):
        request = client.put(
            reverse("user_api:update_email"),
            headers=user_auth_headers,
            data=data_to_update_email
        )

        assert request.status_code == success_resp_data.update["status_code"]
        assert request.data["detail"] == (
            success_resp_data.update["data"]["detail"]
        )

    def test_should_response_auth_headers_error(
            self,
            client,
    ):
        request = client.put(
            reverse("user_api:update_email"),
        )

        assert request.status_code == status.HTTP_401_UNAUTHORIZED
        assert request.data["detail"] == error_resp_data.auth_headers

    def test_should_response_fields_empty_error(
            self,
            client,
            user_auth_headers,
            data_to_update_email_wo_email
    ):
        request = client.put(
            reverse("user_api:update_email"),
            headers=user_auth_headers,
            data=data_to_update_email_wo_email
        )

        assert request.status_code == status.HTTP_400_BAD_REQUEST
        for key in request.data:
            assert request.data[key][0] == error_resp_data.field_is_blank

    def test_should_response_invalid_email_error(
            self,
            client,
            user_auth_headers,
            data_to_update_email_w_invalid_email
    ):
        request = client.put(
            reverse("user_api:update_email"),
            headers=user_auth_headers,
            data=data_to_update_email_w_invalid_email
        )

        assert request.status_code == status.HTTP_400_BAD_REQUEST
        assert request.data["email"][0] == error_resp_data.invalid_email

    def test_should_response_email_already_exist_error(
            self,
            client,
            user_auth_headers,
            data_to_update_email_w_already_exists_email
    ):
        request = client.put(
            reverse("user_api:update_email"),
            headers=user_auth_headers,
            data=data_to_update_email_w_already_exists_email
        )

        assert request.status_code == status.HTTP_400_BAD_REQUEST
        assert request.data["email"][0] == error_resp_data.field_not_unique
