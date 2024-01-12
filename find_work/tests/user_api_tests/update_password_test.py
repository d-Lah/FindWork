import pytest

from django.urls import reverse

from rest_framework import status

from util.user_api_resp.update_password_resp import UpdatePasswordResp


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
        assert request.status_code == status.HTTP_200_OK
        assert request.data["success"] == (
            UpdatePasswordResp.resp_data["successes"][0]["success"]
        )

    def test_should_response_auth_headers_error(
            self,
            client,
    ):
        request = client.put(
            reverse("user_api:update_password"),
        )
        assert request.status_code == status.HTTP_401_UNAUTHORIZED

    def test_should_response_fields_empty_error(
            self,
            client,
            user_auth_headers
    ):
        request = client.put(
            reverse("user_api:update_password"),
            headers=user_auth_headers,
        )
        assert request.status_code == status.HTTP_400_BAD_REQUEST
        assert request.data["error"] == (
            UpdatePasswordResp.resp_data["errors"][0]["error"]
        )
