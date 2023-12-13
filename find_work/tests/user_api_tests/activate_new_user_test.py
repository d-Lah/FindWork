import pytest

from django.urls import reverse

from rest_framework import status

from apps.response_success import ResponseUpdate
from apps.response_error import ResponseUserAlreadyActiveError


@pytest.mark.django_db
class TestActivateNewUser:
    def test_should_activate_user(
            self,
            client,
            data_for_activate_new_user,
    ):
        response = client.put(
            reverse(
                "user_api:activate_new_user",
                kwargs=data_for_activate_new_user
            )
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data.get("status") == (
            ResponseUpdate.response_data["status"]
        )

    def test_should_response_user_already_active_error(
            self,
            client,
            activate_new_user_data_for_response_user_already_active_error,
    ):
        kwargs = activate_new_user_data_for_response_user_already_active_error
        response = client.put(
            reverse(
                "user_api:activate_new_user",
                kwargs=kwargs
            )
        )

        assert response.status_code == status.HTTP_409_CONFLICT
        assert response.data.get("error") == (
            ResponseUserAlreadyActiveError.response_data["error"]
        )
