import pytest

from django.urls import reverse

from rest_framework import status

from util.user_api_resp.register_new_user_resp import RegisterNewUserResp


@pytest.mark.django_db
class TestRegisterNewUser:
    def test_should_register_new_user(
            self,
            mocker,
            client,
            data_to_register_new_user
    ):
        mocker.patch(
            "util.mail_sender.send_mail",
            return_value=True
        )
        response = client.post(
            reverse("user_api:register_new_user"),
            data=data_to_register_new_user
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["success"] == (
            RegisterNewUserResp.resp_data["successes"][0]["success"]
        )

    def test_should_response_fields_empty_error(
            self,
            client,
            data_to_register_new_user_wo_data
    ):
        response = client.post(
            reverse("user_api:register_new_user"),
            data=data_to_register_new_user_wo_data
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["error"] == (
            RegisterNewUserResp.resp_data["errors"][0]["error"]
        )

    def test_should_response_invalid_email_error(
            self,
            client,
            data_to_register_new_user_w_invalid_email
    ):
        response = client.post(
            reverse("user_api:register_new_user"),
            data=data_to_register_new_user_w_invalid_email
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert response.data["error"] == (
            RegisterNewUserResp.resp_data["errors"][1]["error"]
        )

    def test_should_response_email_already_exists_error(
            self,
            client,
            data_to_register_new_user_w_already_exists_email
    ):
        response = client.post(
            reverse("user_api:register_new_user"),
            data=data_to_register_new_user_w_already_exists_email
        )
        assert response.status_code == status.HTTP_409_CONFLICT
        assert response.data["error"][0] == (
            RegisterNewUserResp.resp_data["errors"][2]["error"][0]
        )

    def test_should_response_phone_number_already_exists_error(
            self,
            client,
            data_to_register_new_user_w_already_exists_phone_number
    ):
        response = client.post(
            reverse("user_api:register_new_user"),
            data=data_to_register_new_user_w_already_exists_phone_number
        )
        assert response.status_code == status.HTTP_409_CONFLICT
        assert response.data["error"][0] == (
            RegisterNewUserResp.resp_data["errors"][2]["error"][0]
        )
