import pytest

from django.urls import reverse

from rest_framework import status

from util.user_api_resp.activate_new_user_resp import ActivateNewUserResp


@pytest.mark.django_db
class TestActivateNewUser:
    def test_should_activate_user(
            self,
            client,
            data_to_activate_new_user,
    ):
        request = client.put(
            reverse(
                "user_api:activate_new_user",
                kwargs=data_to_activate_new_user
            )
        )

        assert request.status_code == status.HTTP_200_OK
        assert request.data["success"] == (
            ActivateNewUserResp.resp_data["successes"][0]["success"]
        )

    def test_should_response_user_already_activated_error(
            self,
            client,
            data_to_activate_new_user_w_already_activate_user,
    ):
        request = client.put(
            reverse(
                "user_api:activate_new_user",
                kwargs=data_to_activate_new_user_w_already_activate_user
            )
        )

        assert request.status_code == status.HTTP_409_CONFLICT
        assert request.data["error"] == (
            ActivateNewUserResp.resp_data["errors"][0]["error"]
        )
