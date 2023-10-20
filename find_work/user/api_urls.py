from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import api

app_name = "user_api"


urlpatterns = [
    path(
        "register",
        api.RegisterNewUser.as_view(),
        name="register",
    ),
    path(
        "activate-user/<uuid:user_activation_uuid>",
        api.ActivateUser.as_view(),
        name="activate_user",
    ),
    path(
        "login",
        TokenObtainPairView.as_view(),
        name="login"
    ),
    path(
        "create-2fa-qr-code",
        api.CreateTwoFactorAuthQRCode.as_view(),
        name="create_2fa_qr_code"
    ),
    path(
        "validation-totp-token",
        api.ValidateTOTPToken.as_view(),
        name="validation_totp_token"
    ),
    path(
        "info",
        api.UserInfo.as_view(),
        name="user_info"
    ),
    path(
        "edit-profile-info",
        api.EditProfileInfo.as_view(),
        name="edit_profile_info"
    ),
    path(
        "check-user-password",
        api.CheckUserPassword.as_view(),
        name="check_user_password"
    ),
    path(
        "update-user-password",
        api.UpdateUserPassword.as_view(),
        name="update_user_password"
    )
]
