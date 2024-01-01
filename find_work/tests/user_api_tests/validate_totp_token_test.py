import pytest

from django.urls import reverse

from rest_framework import status

from util.user_api_resp.validate_totp_token_resp import ValidateTOTPTokenResp


@pytest.mark.django_db
class TestValidateTOTPToken:
    def test_should_validate_totp_token(
            self,
            client,
            user_auth_headers,
            data_to_validate_totp_token
    ):
        request = client.post(
            reverse("user_api:validation_totp_token"),
            headers=user_auth_headers,
            data=data_to_validate_totp_token
        )
        assert request.status_code == status.HTTP_200_OK
        assert request.data["success"] == (
            ValidateTOTPTokenResp.resp_data["successes"][0]["success"]
        )

    def test_should_response_auth_headers_error(
            self,
            client,
    ):
        request = client.post(
            reverse("user_api:validation_totp_token"),
        )
        assert request.status_code == status.HTTP_401_UNAUTHORIZED

    def test_should_response_fields_empty_error(
            self,
            client,
            user_auth_headers
    ):
        request = client.post(
            reverse("user_api:validation_totp_token"),
            headers=user_auth_headers,
        )
        assert request.status_code == status.HTTP_400_BAD_REQUEST
        assert request.data["error"] == (
            ValidateTOTPTokenResp.resp_data["errors"][0]["error"]
        )

    def test_should_response_wrong_totp_token_error(
            self,
            client,
            user_auth_headers,
            data_to_validate_totp_token_w_wrong_totp_token
    ):
        request = client.post(
            reverse("user_api:validation_totp_token"),
            headers=user_auth_headers,
            data=data_to_validate_totp_token_w_wrong_totp_token
        )
        assert request.status_code == status.HTTP_403_FORBIDDEN
        assert request.data["error"] == (
            ValidateTOTPTokenResp.resp_data["errors"][1]["error"]
        )
