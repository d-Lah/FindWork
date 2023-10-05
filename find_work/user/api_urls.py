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
        api.Register.as_view(),
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
        api.ValidationTOTPToken.as_view(),
        name="validation_totp_token"
    )
]
