import pytest

from django.urls import reverse

from rest_framework import status

from util import error_resp_data
from util import success_resp_data


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

        assert request.status_code == success_resp_data.update["status_code"]
        assert request.data["detail"] == (
            success_resp_data.update["data"]["detail"]
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
        assert request.data["detail"] == (
            error_resp_data.user_activation_uuid_incap
        )
