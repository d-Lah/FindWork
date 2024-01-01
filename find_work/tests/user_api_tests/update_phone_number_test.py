import pytest

from django.urls import reverse

from rest_framework import status

from util.user_api_resp.update_phone_number_resp import UpdatePhoneNumberResp


@pytest.mark.django_db
class TestupdatePhoneNumber:
    def test_should_update_phone_number(
            self,
            client,
            user_auth_headers,
            data_to_update_phone_number
    ):
        request = client.put(
            reverse("user_api:update_phone_number"),
            headers=user_auth_headers,
            data=data_to_update_phone_number
        )
        assert request.status_code == status.HTTP_200_OK
        assert request.data["success"] == (
            UpdatePhoneNumberResp.resp_data["successes"][0]["success"]
        )

    def test_should_response_auth_headers_error(
            self,
            client,
    ):
        request = client.put(
            reverse("user_api:update_phone_number"),
        )
        assert request.status_code == status.HTTP_401_UNAUTHORIZED

    def test_should_response_fields_empty_error(
            self,
            client,
            user_auth_headers,
            data_to_update_phone_number_wo_phone_number
    ):
        request = client.put(
            reverse("user_api:update_phone_number"),
            headers=user_auth_headers,
            data=data_to_update_phone_number_wo_phone_number
        )
        assert request.status_code == status.HTTP_400_BAD_REQUEST
        assert request.data["error"] == (
            UpdatePhoneNumberResp.resp_data["errors"][0]["error"]
        )

    def test_should_response_phone_number_already_exists_error(
            self,
            client,
            user_auth_headers,
            data_to_update_phone_number_w_already_exists_phone_number
    ):
        request = client.put(
            reverse("user_api:update_phone_number"),
            headers=user_auth_headers,
            data=data_to_update_phone_number_w_already_exists_phone_number
        )
        assert request.status_code == status.HTTP_409_CONFLICT
        assert request.data["error"] == (
            UpdatePhoneNumberResp.resp_data["errors"][1]["error"]
        )
