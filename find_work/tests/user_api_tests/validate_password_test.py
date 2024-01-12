import pytest

from django.urls import reverse

from rest_framework import status

from util.user_api_resp.validate_password_resp import ValidatePasswordResp


@pytest.mark.django_db
class TestValidatePassword:
    def test_should_validate_password(
        self,
        client,
        user_auth_headers,
        data_to_validate_password
    ):
        request = client.post(
            reverse("user_api:validate_password"),
            headers=user_auth_headers,
            data=data_to_validate_password
        )
        assert request.status_code == status.HTTP_200_OK
        assert request.data["success"] == (
            ValidatePasswordResp.resp_data["successes"][0]["success"]
        )

    def test_should_response_auth_headers_error(
        self,
        client,
    ):
        request = client.post(
            reverse("user_api:validate_password"),
        )
        assert request.status_code == status.HTTP_401_UNAUTHORIZED

    def test_should_response_fields_empty_error(
        self,
        client,
        user_auth_headers
    ):
        request = client.post(
            reverse("user_api:validate_password"),
            headers=user_auth_headers
        )
        assert request.status_code == status.HTTP_400_BAD_REQUEST
        assert request.data["error"] == (
            ValidatePasswordResp.resp_data["errors"][0]["error"]
        )

    def test_should_response_wrong_password_error(
        self,
        client,
        user_auth_headers,
        data_to_validate_password_w_wrong_password,
    ):
        request = client.post(
            reverse("user_api:validate_password"),
            headers=user_auth_headers,
            data=data_to_validate_password_w_wrong_password
        )
        assert request.status_code == status.HTTP_403_FORBIDDEN
        assert request.data["error"] == (
            ValidatePasswordResp.resp_data["errors"][1]["error"]
        )
