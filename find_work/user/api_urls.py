from . import (
    api,
)
from django.urls import (
    path,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

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
]
