from django.urls import path

from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenObtainPairView,
)
from .api.user_info import UserInfo
from .api.activate_new_user import ActivateUser
from .api.register_new_user import RegisterNewUser
from .api.edit_profile_info import EditProfileInfo
from .api.update_user_email import UpdateUserEmail
from .api.upload_user_avatar import UploadUserAvatar
from .api.check_user_password import CheckUserPassword
from .api.reset_user_password import ResetUserPassword
from .api.validate_totp_token import ValidateTOTPToken
from .api.update_user_password import UpdateUserPassword
from .api.update_user_phone_number import UpdateUserPhoneNumber
from .api.activate_two_factor_auth import ActivateTwoFactorAuth
from .api.get_two_factor_auth_qr_code import GetTwoFactorAuthQRCode
from .api.generate_user_reset_password_totp import GenerateUserResetPasswordTOTP
from .api.validate_user_reset_password_totp import ValidateUserResetPasswordTOTP

app_name = "user_api"


urlpatterns = [
    path(
        "register",
        RegisterNewUser.as_view(),
        name="register_new_user",
    ),
    path(
        "activate-user/<uuid:user_activation_uuid>",
        ActivateUser.as_view(),
        name="activate_new_user",
    ),
    path(
        "login",
        TokenObtainPairView.as_view(),
        name="login_user"
    ),
    path(
        "create-2fa-qr-code",
        GetTwoFactorAuthQRCode.as_view(),
        name="create_2fa_qr_code"
    ),
    path(
        "validation-totp-token",
        ValidateTOTPToken.as_view(),
        name="validation_totp_token"
    ),
    path(
        "activate_two_factor_auth",
        ActivateTwoFactorAuth.as_view(),
        name="activate_two_factor_auth"
    ),
    path(
        "info",
        UserInfo.as_view(),
        name="user_info"
    ),
    path(
        "edit-profile-info",
        EditProfileInfo.as_view(),
        name="edit_profile_info"
    ),
    path(
        "check-user-password",
        CheckUserPassword.as_view(),
        name="check_user_password"
    ),
    path(
        "update-user-password",
        UpdateUserPassword.as_view(),
        name="update_user_password"
    ),
    path(
        "update-user-email",
        UpdateUserEmail.as_view(),
        name="update_user_email"
    ),
    path(
        "update-user-phone-number",
        UpdateUserPhoneNumber.as_view(),
        name="update_user_phone_number"
    ),
    path(
        "upload-user-avatar",
        UploadUserAvatar.as_view(),
        name="upload_user_avatar"
    ),
    path(
        "generate-user-reset-password-uuid",
        GenerateUserResetPasswordTOTP.as_view(),
        name="generate_user_reset_password_totp"
    ),
    path(
        "validate-user-reset-password-uuid",
        ValidateUserResetPasswordTOTP.as_view(),
        name="validate_user_reset_password_totp"
    ),
    path(
        "reset-user-password",
        ResetUserPassword.as_view(),
        name="reset_user_password"
    ),
]
