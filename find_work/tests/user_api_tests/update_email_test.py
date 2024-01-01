import pytest

from django.urls import reverse

from rest_framework import status

from util.user_api_resp.update_email_resp import UpdateEmailResp


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
        assert request.status_code == status.HTTP_200_OK
        assert request.data["success"] == (
            UpdateEmailResp.resp_data["successes"][0]["success"]
        )

    def test_should_response_auth_headers_error(
            self,
            client,
    ):
        request = client.put(
            reverse("user_api:update_email"),
        )
        assert request.status_code == status.HTTP_401_UNAUTHORIZED

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
        assert request.data["error"] == (
            UpdateEmailResp.resp_data["errors"][0]["error"]
        )

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
        assert request.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert request.data["error"] == (
            UpdateEmailResp.resp_data["errors"][1]["error"]
        )

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
        assert request.status_code == status.HTTP_409_CONFLICT
        assert request.data["error"] == (
            UpdateEmailResp.resp_data["errors"][2]["error"]
        )
