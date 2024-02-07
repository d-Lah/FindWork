import pytest

from django.urls import reverse

from util.success_resp_data import UpdateSuccess
from util.error_resp_data import UserActivateUUIDIncapError


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

        assert request.status_code == UpdateSuccess().get_status()
        assert request.data["success"] == (
            UpdateSuccess().get_data()["success"]
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

        assert request.status_code == UserActivateUUIDIncapError().get_status()
        assert request.data["user_activate_uuid"] == (
            UserActivateUUIDIncapError().get_data()["user_activate_uuid"]
        )
