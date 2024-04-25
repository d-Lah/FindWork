import pytest

from django.urls import reverse

from rest_framework import status

from util import error_resp_data
from util import success_resp_data


@pytest.mark.django_db
class TestValidateTOTPToken:
    def test_should_validate_totp(
            self,
            client,
            user_auth_headers,
            data_to_validate_totp
    ):
        request = client.post(
            reverse("user_api:validation_totp"),
            headers=user_auth_headers,
            data=data_to_validate_totp
        )

        assert request.status_code == success_resp_data.validate["status_code"]
        assert request.data["detail"] == (
            success_resp_data.validate["data"]["detail"]
        )

    def test_should_response_auth_headers_error(
            self,
            client,
    ):
        request = client.post(
            reverse("user_api:validation_totp"),
        )

        assert request.status_code == status.HTTP_401_UNAUTHORIZED
        assert request.data["detail"] == (
            error_resp_data.auth_headers
        )

    def test_should_response_fields_empty_error(
            self,
            client,
            user_auth_headers,
            data_to_validate_totp_wo_data
    ):
        request = client.post(
            reverse("user_api:validation_totp"),
            headers=user_auth_headers,
            data=data_to_validate_totp_wo_data
        )

        assert request.status_code == status.HTTP_400_BAD_REQUEST
        assert request.data["totp"][0] == error_resp_data.field_is_blank

    def test_should_response_totp_incap_error(
            self,
            client,
            user_auth_headers,
            data_to_validate_totp_w_totp_incap
    ):
        request = client.post(
            reverse("user_api:validation_totp"),
            headers=user_auth_headers,
            data=data_to_validate_totp_w_totp_incap
        )

        assert request.status_code == status.HTTP_403_FORBIDDEN
        assert request.data["detail"] == error_resp_data.totp_incap
