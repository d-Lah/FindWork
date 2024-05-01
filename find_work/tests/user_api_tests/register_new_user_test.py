import pytest

from django.urls import reverse

from rest_framework import status

from util import error_resp_data
from util import success_resp_data


@pytest.mark.django_db
class TestRegisterNewUser:
    def test_should_register_new_user(
            self,
            mocker,
            client,
            data_to_register_new_user
    ):
        mocker.patch(
            "util.mail_sender.send_mail",
            return_value=True
        )
        request = client.post(
            reverse("user_api:register_new_user"),
            data=data_to_register_new_user
        )

        assert request.status_code == success_resp_data.create["status_code"]
        assert request.data["detail"] == (
            success_resp_data.create["data"]["detail"]
        )

    def test_should_response_fields_empty_error(
            self,
            client,
            data_to_register_new_user_wo_data
    ):
        request = client.post(
            reverse("user_api:register_new_user"),
            data=data_to_register_new_user_wo_data
        )

        assert request.status_code == status.HTTP_400_BAD_REQUEST
        for key in request.data:
            assert (
                request.data[key][0] == error_resp_data.field_is_blank
                or request.data[key][0] == error_resp_data.field_not_boolean
            )

    def test_should_response_invalid_email_error(
            self,
            client,
            data_to_register_new_user_w_invalid_email
    ):
        request = client.post(
            reverse("user_api:register_new_user"),
            data=data_to_register_new_user_w_invalid_email
        )

        assert request.status_code == status.HTTP_400_BAD_REQUEST
        assert request.data["email"][0] == error_resp_data.invalid_email

    def test_should_response_email_already_exists_error(
            self,
            client,
            data_to_register_new_user_w_already_exists_email
    ):
        request = client.post(
            reverse("user_api:register_new_user"),
            data=data_to_register_new_user_w_already_exists_email
        )

        assert request.status_code == status.HTTP_400_BAD_REQUEST
        assert request.data["email"][0] == error_resp_data.field_not_unique
