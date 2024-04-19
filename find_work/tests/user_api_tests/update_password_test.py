import pytest

from django.urls import reverse

from rest_framework import status

from util import error_resp_data
from util import success_resp_data


@pytest.mark.django_db
class TestUpdatePassword:
    def test_should_update_password(
            self,
            client,
            mocker,
            user_auth_headers,
            data_to_update_password
    ):
        mocker.patch(
            "util.mail_sender.send_mail",
            return_value=True
        )

        request = client.put(
            reverse("user_api:update_password"),
            headers=user_auth_headers,
            data=data_to_update_password
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
            reverse("user_api:update_password"),
        )

        assert request.status_code == status.HTTP_401_UNAUTHORIZED
        assert request.data["detail"] == error_resp_data.auth_headers

    def test_should_response_fields_empty_error(
            self,
            client,
            user_auth_headers,
            data_to_update_password_wo_data,
    ):
        request = client.put(
            reverse("user_api:update_password"),
            headers=user_auth_headers,
            data=data_to_update_password_wo_data
        )

        assert request.status_code == status.HTTP_400_BAD_REQUEST
        for field in request.data:
            assert request.data[field][0] == error_resp_data.field_is_blank

    def test_should_response_wrong_password_error(
        self,
        client,
        user_auth_headers,
        data_to_update_password_w_wrong_old_password,
    ):
        request = client.put(
            reverse("user_api:update_password"),
            headers=user_auth_headers,
            data=data_to_update_password_w_wrong_old_password
        )

        assert request.status_code == status.HTTP_403_FORBIDDEN
        assert request.data["detail"] == error_resp_data.wrong_password
