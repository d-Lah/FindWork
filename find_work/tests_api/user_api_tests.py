import pytest
from django.urls import reverse
# Create your tests here.


@pytest.mark.django_db
class TestClassUser:
    def test_should_register_user(
            self,
            mocker,
            client,
            data_for_test_register_user):

        mocker.patch(
            "django.core.mail.send_mail",
            return_value="return Response({'status':'Success'}, status=201)"
        )
        response = client.post(
            reverse("user_api:register"),
            data=data_for_test_register_user
        )
        assert response.status_code == 201
        assert response.data.get("status") == "Success"

    def test_should_response_user_field_empty_error_in_register(
            self,
            client,
            data_for_test_user_field_empty_error):

        response = client.post(
            reverse("user_api:register"),
            data=data_for_test_user_field_empty_error
        )
        assert response.status_code == 400
        assert response.data.get("error") == "UserFieldEmptyError"

    def test_should_response_profile_field_empty_error_in_register(
            self,
            client,
            data_for_test_profile_field_empty_error):

        response = client.post(
            reverse("user_api:register"),
            data=data_for_test_profile_field_empty_error
        )
        assert response.status_code == 400
        assert response.data.get("error") == "ProfileFieldEmptyError"

    def test_should_response_email_already_exists_error_in_register(
            self,
            client,
            data_for_test_email_already_exists_error):

        response = client.post(
            reverse("user_api:register"),
            data=data_for_test_email_already_exists_error
        )
        assert response.status_code == 409
        assert response.data.get("error") == "EmailAlreadyExists"

    def test_should_response_phone_number_already_exists_error_in_register(
            self,
            client,
            data_for_test_phone_number_already_exists_error):

        response = client.post(
            reverse("user_api:register"),
            data=data_for_test_phone_number_already_exists_error
        )
        assert response.status_code == 409
        assert response.data.get("error") == "PhoneNumberAlreadyExistsError"
