import pytest

from django.urls import reverse

from rest_framework import status

from util import error_resp_data
from util import success_resp_data


@pytest.mark.django_db
class TestResetPassword:
    def test_should_reset_password(
            self,
            client,
            data_to_reset_password
    ):
        request = client.put(
            reverse("user_api:reset_password"),
            data=data_to_reset_password
        )
        assert request.status_code == success_resp_data.update["status_code"]
        assert request.data["detail"] == (
            success_resp_data.update["data"]["detail"]
        )

    def test_should_response_fields_empty_error(
            self,
            client,
            data_to_reset_password_wo_data
    ):
        request = client.put(
            reverse("user_api:reset_password"),
            data=data_to_reset_password_wo_data
        )
        assert request.status_code == status.HTTP_400_BAD_REQUEST
        for key in request.data:
            assert request.data[key][0] == error_resp_data.field_is_blank

    def test_should_response_invalid_email_error(
            self,
            client,
            data_to_reset_password_w_invalid_email
    ):
        request = client.put(
            reverse("user_api:reset_password"),
            data=data_to_reset_password_w_invalid_email

        )
        assert request.status_code == status.HTTP_400_BAD_REQUEST
        assert request.data["email"][0] == error_resp_data.invalid_email

    def test_should_response_user_not_found_error(
            self,
            client,
            data_to_reset_password_w_wrong_email
    ):
        request = client.put(
            reverse("user_api:reset_password"),
            data=data_to_reset_password_w_wrong_email
        )
        assert request.status_code == status.HTTP_404_NOT_FOUND
        assert request.data["detail"] == (
            error_resp_data.user_with_given_email_not_found
        )
