from django.urls import path

from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenObtainPairView,
)

from .api.user_info import UserInfo
from .api.update_email import UpdateEmail
from .api.profile_info import ProfileInfo
from .api.upload_avatar import UploadAvatar
from .api.reset_password import ResetPassword
from .api.update_password import UpdatePassword
from .api.activate_new_user import ActivateNewUser
from .api.register_new_user import RegisterNewUser
from .api.edit_profile_info import EditProfileInfo
from .api.validate_password import ValidatePassword
from .api.update_phone_number import UpdatePhoneNumber
from .api.validate_totp_token import ValidateTOTPToken
from .api.edit_employee_profile_specialization import (
    EditEmployeeProfileSpecialization
)
from .api.activate_two_factor_auth import ActivateTwoFactorAuth
from .api.deactivate_two_factor_auth import DeactivateTwoFactorAuth
from .api.get_two_factor_auth_qr_code import GetTwoFactorAuthQRCode
from .api.get_employee_specialization import GetEmployeeSpecialization
from .api.generate_reset_password_totp import GenerateResetPasswordTOTP
from .api.validate_reset_password_totp import ValidateResetPasswordTOTP

app_name = "user_api"

urlpatterns = [
    path(
        "register",
        RegisterNewUser.as_view(),
        name="register_new_user",
    ),
    path(
        "activate-user/<uuid:user_activation_uuid>",
        ActivateNewUser.as_view(),
        name="activate_new_user",
    ),
    path(
        "login",
        TokenObtainPairView.as_view(),
        name="login_user"
    ),
    path(
        "get-two-factor_auth-qr-code",
        GetTwoFactorAuthQRCode.as_view(),
        name="get_two_factor_auth_qr_code"
    ),
    path(
        "validation-totp-token",
        ValidateTOTPToken.as_view(),
        name="validation_totp_token"
    ),
    path(
        "activate-two-factor-auth",
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
        "validate-password",
        ValidatePassword.as_view(),
        name="validate_password"
    ),
    path(
        "update-password",
        UpdatePassword.as_view(),
        name="update_password"
    ),
    path(
        "update-email",
        UpdateEmail.as_view(),
        name="update_email"
    ),
    path(
        "update-phone-number",
        UpdatePhoneNumber.as_view(),
        name="update_phone_number"
    ),
    path(
        "upload-avatar",
        UploadAvatar.as_view(),
        name="upload_avatar"
    ),
    path(
        "generate-reset-password-totp",
        GenerateResetPasswordTOTP.as_view(),
        name="generate_reset_password_totp"
    ),
    path(
        "validate-reset-password-uuid",
        ValidateResetPasswordTOTP.as_view(),
        name="validate_reset_password_totp"
    ),
    path(
        "reset-password",
        ResetPassword.as_view(),
        name="reset_password"
    ),
    path(
        "profile-info",
        ProfileInfo.as_view(),
        name="profile_info"
    ),
    path(
        "deactivate-two-factor-auth",
        DeactivateTwoFactorAuth.as_view(),
        name="deactivate_two_factor_auth"
    ),
    path(
        "edit-employee-profile-specialization",
        EditEmployeeProfileSpecialization.as_view(),
        name="edit_employee_profile_specialization"
    ),
    path(
        "get-employee-specialization",
        GetEmployeeSpecialization.as_view(),
        name="get_employee_specialization"
    ),
]
