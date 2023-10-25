import pytest

from django.urls import reverse

from rest_framework import status

from user.models import (
    Profile,
    UserAvatar,
)
from find_work.settings import BASE_DIR
from apps.response_error import (
    ResponseWrongPasswordError,
    ResponseUserFieldEmptyError,
    ResponseWrongTOTPTokenError,
    ResponseEmailFieldEmptyError,
    ResponseInvalidImageExtError,
    ResponseImageSizeTooLargeError,
    ResponseProfileFieldEmptyError,
    ResponseUserAlreadyActiveError,
    ResponsePasswordFieldEmptyError,
    ResponseEmailAlreadyExistsError,
    ResponseTOTPTokenFieldEmptyError,
    ResponseUserAvatarFieldEmptyError,
    ResponsePhoneNumberFieldEmptyError,
    ResponsePhoneNumberAlreadyExistsError,
    ResponseTwoFactorAuthAlreadyActiveError,
)
from apps.response_success import (
    ResponseGet,
    ResponseValid,
    ResponseCreate,
    ResponseUpdate,
    ResponseUpload,
)


@pytest.mark.django_db
class TestClassUser:
    def test_should_register_user(
            self,
            mocker,
            client,
            data_for_test_register_user,
    ):
        mocker.patch(
            "django.core.mail.send_mail",
            return_value="return ResponseCreate().get_response()",
        )
        response = client.post(
            reverse("user_api:register"),
            data=data_for_test_register_user,
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data.get("status") == ResponseCreate.response_data["status"]

    def test_should_response_user_field_empty_error_in_register_api(
            self,
            client,
            data_for_test_user_field_empty_error,
    ):
        response = client.post(
            reverse("user_api:register"),
            data=data_for_test_user_field_empty_error,
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data.get("error") == (
            ResponseUserFieldEmptyError.response_data["error"]
        )

    def test_should_response_profile_field_empty_error_in_register_api(
            self,
            client,
            data_for_test_profile_field_empty_error,
    ):
        response = client.post(
            reverse("user_api:register"),
            data=data_for_test_profile_field_empty_error,
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data.get("error") == (
            ResponseProfileFieldEmptyError.response_data["error"]
        )

    def test_should_response_email_already_exists_error_in_register_api(
            self,
            client,
            data_for_test_email_already_exists_error,
    ):
        response = client.post(
            reverse("user_api:register"),
            data=data_for_test_email_already_exists_error,
        )
        assert response.status_code == status.HTTP_409_CONFLICT
        assert response.data.get("error") == (
            ResponseEmailAlreadyExistsError.response_data["error"]
        )

    def test_should_response_phone_number_already_exists_error_in_register_api(
            self,
            client,
            data_for_test_phone_number_already_exists_error,
    ):
        response = client.post(
            reverse("user_api:register"),
            data=data_for_test_phone_number_already_exists_error,
        )
        assert response.status_code == status.HTTP_409_CONFLICT
        assert response.data.get("error") == (
            ResponsePhoneNumberAlreadyExistsError.response_data["error"]
        )

    def test_should_activate_user(
            self,
            client,
            data_for_test_activate_user,
    ):
        kwargs = {
            "user_activation_uuid": data_for_test_activate_user
        }
        response = client.put(
            reverse(
                "user_api:activate_user",
                kwargs=kwargs
            )
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data.get("status") == ResponseUpdate.response_data["status"]

    def test_should_response_user_already_active_error_in_activate_user_api(
            self,
            client,
            data_for_test_user_already_active_error,
    ):
        kwargs = {
            "user_activation_uuid": data_for_test_user_already_active_error
        }
        response = client.put(
            reverse(
                "user_api:activate_user",
                kwargs=kwargs
            )
        )

        assert response.status_code == status.HTTP_409_CONFLICT
        assert response.data.get("error") == (
            ResponseUserAlreadyActiveError.response_data["error"]
        )

    def test_should_login_user(
            self,
            client,
            data_for_test_login_user
    ):
        response = client.post(
            reverse("user_api:login"),
            data=data_for_test_login_user
        )
        assert response.status_code == status.HTTP_200_OK

    def test_should_response_user_not_active_error_in_login_api(
            self,
            client,
            data_for_test_response_user_not_active_error
    ):
        response = client.post(
            reverse("user_api:login"),
            data=data_for_test_response_user_not_active_error,
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_should_response_field_empty_error_in_login_api(
            self,
            client,
            data_for_test_response_field_empty_error
    ):
        response = client.post(
            reverse("user_api:login"),
            data=data_for_test_response_field_empty_error,
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_should_create_two_factor_auth_qr_code(
            self,
            client,
            user_auth_headers,
            data_for_test_should_create_two_factor_auth_qr_code
    ):
        request = client.post(
            reverse("user_api:create_2fa_qr_code"),
            headers=user_auth_headers,
            data=data_for_test_should_create_two_factor_auth_qr_code
        )
        assert request.status_code == status.HTTP_201_CREATED
        assert request.data.get("status") == ResponseCreate.response_data["status"]

    def test_should_response_auth_headers_error_in_create_2fa_qr_code(
            self,
            client,
            data_for_test_should_create_two_factor_auth_qr_code
    ):
        request = client.post(
            reverse("user_api:create_2fa_qr_code"),
            data=data_for_test_should_create_two_factor_auth_qr_code
        )
        assert request.status_code == status.HTTP_401_UNAUTHORIZED

    def test_should_validate_totp_token(
            self,
            client,
            user_auth_headers,
            data_for_test_validate_totp_token
    ):
        request = client.post(
            reverse("user_api:validation_totp_token"),
            headers=user_auth_headers,
            data=data_for_test_validate_totp_token
        )
        assert request.status_code == status.HTTP_200_OK
        assert request.data.get("status") == ResponseValid.response_data["status"]

    def test_should_response_auth_headers_error_in_validate_totp_token(
            self,
            client,
            data_for_test_validate_totp_token,
    ):
        request = client.post(
            reverse("user_api:validation_totp_token"),
            data=data_for_test_validate_totp_token
        )
        assert request.status_code == status.HTTP_401_UNAUTHORIZED

    def test_should_response_totp_token_field_empty_error_in_validate_totp_token(
            self,
            client,
            user_auth_headers
    ):
        request = client.post(
            reverse("user_api:validation_totp_token"),
            headers=user_auth_headers,
        )
        assert request.status_code == status.HTTP_400_BAD_REQUEST
        assert request.data.get("error") == (
            ResponseTOTPTokenFieldEmptyError.response_data["error"]
        )

    def test_should_response_wrong_totp_token_error(
            self,
            client,
            user_auth_headers,
            data_for_test_should_response_wrong_totp_token_error
    ):
        request = client.post(
            reverse("user_api:validation_totp_token"),
            headers=user_auth_headers,
            data=data_for_test_should_response_wrong_totp_token_error
        )
        assert request.status_code == status.HTTP_401_UNAUTHORIZED
        assert request.data.get("error") == (
            ResponseWrongTOTPTokenError.response_data["error"]
        )

    def test_should_activate_two_factor_auth(
            self,
            client,
            user_auth_headers
    ):
        request = client.put(
            reverse("user_api:activate_two_factor_auth"),
            headers=user_auth_headers
        )

        assert request.status_code == status.HTTP_200_OK
        assert request.data.get("status") == ResponseUpdate.response_data["status"]

    def test_should_response_auth_headers_error_in_activate_two_factor_auth(
            self,
            client,
    ):
        request = client.put(
            reverse("user_api:activate_two_factor_auth"),
        )

        assert request.status_code == status.HTTP_401_UNAUTHORIZED

    def test_should_response_two_factor_auth_already_active_error(
            self,
            client,
            user_auth_headers_with_already_active_two_factor_auth
    ):
        request = client.put(
            reverse("user_api:activate_two_factor_auth"),
            headers=user_auth_headers_with_already_active_two_factor_auth
        )

        assert request.status_code == status.HTTP_409_CONFLICT
        assert request.data.get("error") == (
            ResponseTwoFactorAuthAlreadyActiveError.response_data["error"]
        )

    def test_should_get_user_info(
            self,
            client,
            user_auth_headers
    ):
        request = client.get(
            reverse("user_api:user_info"),
            headers=user_auth_headers
        )
        assert request.status_code == status.HTTP_200_OK
        assert request.data.get("status") == ResponseGet.response_data["status"]

    def test_should_response_auth_headers_error_in_user_info(
            self,
            client
    ):
        request = client.get(
            reverse("user_api:user_info"),
        )
        assert request.status_code == status.HTTP_401_UNAUTHORIZED

    def test_should_edit_profile_info(
            self,
            client,
            user_auth_headers,
            data_for_test_should_edit_profile_info
    ):
        request = client.put(
            reverse("user_api:edit_profile_info"),
            headers=user_auth_headers,
            data=data_for_test_should_edit_profile_info
        )
        assert request.status_code == status.HTTP_200_OK
        assert request.data.get("status") == ResponseUpdate.response_data["status"]

    def test_should_response_auth_headers_error_in_edit_profile_info(
            self,
            client,
            data_for_test_should_edit_profile_info
    ):
        request = client.put(
            reverse("user_api:edit_profile_info"),
            data=data_for_test_should_edit_profile_info
        )
        assert request.status_code == status.HTTP_401_UNAUTHORIZED

    def test_should_response_profile_field_empty_error_in_edit_profile_info(
            self,
            client,
            user_auth_headers,
    ):
        request = client.put(
            reverse("user_api:edit_profile_info"),
            headers=user_auth_headers
        )
        assert request.status_code == status.HTTP_400_BAD_REQUEST
        assert request.data.get("error") == (
            ResponseProfileFieldEmptyError.response_data["error"]
        )

    def test_should_check_user_password(
            self,
            client,
            user_auth_headers,
            data_for_test_should_check_user_password
    ):
        request = client.post(
            reverse("user_api:check_user_password"),
            headers=user_auth_headers,
            data=data_for_test_should_check_user_password
        )
        assert request.status_code == status.HTTP_200_OK
        assert request.data.get("status") == ResponseValid.response_data["status"]

    def test_should_response_auth_headers_error_in_check_user_password(
            self,
            client,
            data_for_test_should_check_user_password
    ):
        request = client.post(
            reverse("user_api:check_user_password"),
            data=data_for_test_should_check_user_password
        )
        assert request.status_code == status.HTTP_401_UNAUTHORIZED

    def test_should_response_password_field_empty_error_in_check_user_password(
            self,
            client,
            user_auth_headers
    ):
        request = client.post(
            reverse("user_api:check_user_password"),
            headers=user_auth_headers
        )
        assert request.status_code == status.HTTP_400_BAD_REQUEST
        assert request.data.get("error") == (
            ResponsePasswordFieldEmptyError.response_data["error"]
        )

    def test_should_response_wrong_password_error(
            self,
            client,
            user_auth_headers,
            data_for_test_should_response_wrong_password_error,
    ):
        request = client.post(
            reverse("user_api:check_user_password"),
            headers=user_auth_headers,
            data=data_for_test_should_response_wrong_password_error
        )
        assert request.status_code == status.HTTP_401_UNAUTHORIZED
        assert request.data.get("error") == (
            ResponseWrongPasswordError.response_data["error"]
        )

    def test_should_update_user_password(
            self,
            client,
            user_auth_headers,
            data_for_test_should_update_user_password
    ):
        request = client.put(
            reverse("user_api:update_user_password"),
            headers=user_auth_headers,
            data=data_for_test_should_update_user_password
        )
        assert request.status_code == status.HTTP_200_OK
        assert request.data.get("status") == ResponseUpdate.response_data["status"]

    def test_should_response_auth_headers_error_in_update_user_password(
            self,
            client,
            data_for_test_should_update_user_password
    ):
        request = client.put(
            reverse("user_api:update_user_password"),
            data=data_for_test_should_update_user_password
        )
        assert request.status_code == status.HTTP_401_UNAUTHORIZED

    def test_should_response_password_field_empty_error_in_update_user_password(
            self,
            client,
            user_auth_headers
    ):
        request = client.put(
            reverse("user_api:update_user_password"),
            headers=user_auth_headers,
        )
        assert request.status_code == status.HTTP_400_BAD_REQUEST
        assert request.data.get("error") == (
            ResponsePasswordFieldEmptyError.response_data["error"]
        )

    def test_should_update_user_email(
            self,
            client,
            user_auth_headers,
            data_for_test_should_update_user_email
    ):
        request = client.put(
            reverse("user_api:update_user_email"),
            headers=user_auth_headers,
            data=data_for_test_should_update_user_email
        )
        assert request.status_code == status.HTTP_200_OK
        assert request.data.get("status") == ResponseUpdate.response_data["status"]

    def test_should_response_auth_headers_error_in_update_user_email(
            self,
            client,
            data_for_test_should_update_user_email
    ):
        request = client.put(
            reverse("user_api:update_user_email"),
            data=data_for_test_should_update_user_email
        )
        assert request.status_code == status.HTTP_401_UNAUTHORIZED

    def test_should_response_email_field_empty_error_in_update_user_email(
            self,
            client,
            user_auth_headers,
    ):
        request = client.put(
            reverse("user_api:update_user_email"),
            headers=user_auth_headers
        )
        assert request.status_code == status.HTTP_400_BAD_REQUEST
        assert request.data.get("error") == (
            ResponseEmailFieldEmptyError.response_data["error"]
        )

    def test_should_update_user_phone_number(
            self,
            client,
            user_auth_headers,
            data_for_test_should_update_user_phone_number
    ):
        request = client.put(
            reverse("user_api:update_user_phone_number"),
            headers=user_auth_headers,
            data=data_for_test_should_update_user_phone_number
        )
        assert request.status_code == status.HTTP_200_OK
        assert request.data.get("status") == ResponseUpdate.response_data["status"]

    def test_should_response_auth_headers_error_in_update_user_phone_number(
            self,
            client,
            data_for_test_should_update_user_phone_number
    ):
        request = client.put(
            reverse("user_api:update_user_phone_number"),
            data=data_for_test_should_update_user_phone_number
        )
        assert request.status_code == status.HTTP_401_UNAUTHORIZED

    def test_should_response_phone_number_field_empty_error_update_user_phone_number(
            self,
            client,
            user_auth_headers,
    ):
        request = client.put(
            reverse("user_api:update_user_phone_number"),
            headers=user_auth_headers,
        )
        assert request.status_code == status.HTTP_400_BAD_REQUEST
        assert request.data.get("error") == (
            ResponsePhoneNumberFieldEmptyError.response_data["error"]
        )

    def test_should_upload_user_avatar(
            self,
            client,
            mocker,
            user_auth_headers,
            data_for_test_should_upload_user_avatar
    ):
        mocker.patch.object(
            Profile,
            "save",
            return_value="return ResponseUpload().get_response()")
        mocker.patch.object(
            UserAvatar,
            "save",
            return_value="return ResponseUpload().get_response()"
        )

        request = client.post(
            reverse("user_api:upload_user_avatar"),
            headers=user_auth_headers,
            data=data_for_test_should_upload_user_avatar
        )
        assert request.status_code == status.HTTP_201_CREATED
        assert request.data.get("status") == ResponseUpload.response_data["status"]

    def test_should_response_auth_headers_error_in_upload_user_avatar(
            self,
            client,
    ):
        request = client.post(
            reverse("user_api:upload_user_avatar"),
        )
        assert request.status_code == status.HTTP_401_UNAUTHORIZED

    def test_should_response_user_avatar_field_empty_error(
            self,
            client,
            user_auth_headers
    ):
        request = client.post(
            reverse("user_api:upload_user_avatar"),
            headers=user_auth_headers,
        )
        assert request.status_code == status.HTTP_400_BAD_REQUEST
        assert request.data.get("error") == (
            ResponseUserAvatarFieldEmptyError.response_data["error"]
        )

    def test_should_response_image_size_too_large_in_upload_user_avatar(
            self,
            client,
            user_auth_headers,
            data_for_test_should_response_image_size_too_large_error
    ):
        request = client.post(
            reverse("user_api:upload_user_avatar"),
            headers=user_auth_headers,
            data=data_for_test_should_response_image_size_too_large_error
        )
        assert request.status_code == status.HTTP_413_REQUEST_ENTITY_TOO_LARGE
        assert request.data.get("error") == (
            ResponseImageSizeTooLargeError.response_data["error"]
        )

    def test_should_response_invalid_image_ext(
            self,
            client,
            user_auth_headers,
            data_for_test_should_resonse_invalid_image_ext_error
    ):
        request = client.post(
            reverse("user_api:upload_user_avatar"),
            headers=user_auth_headers,
            data=data_for_test_should_resonse_invalid_image_ext_error
        )
        assert request.status_code == status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
        assert request.data.get("error") == (
            ResponseInvalidImageExtError.response_data["error"]
        )
