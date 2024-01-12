from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from user.models import User

from util.user_api_resp.activate_two_factor_auth_resp import (
    ActivateTwoFactorAuthResp
)


class ActivateTwoFactorAuth(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(
            self,
            request
    ):
        user_id = request.user.id

        user = User.objects.filter(
            pk=user_id,
            is_two_factor_auth=False
        ).first()

        if not user:
            return ActivateTwoFactorAuthResp(
            ).resp_two_factor_auth_already_activated_error()

        user.is_two_factor_auth = True
        user.save()

        return ActivateTwoFactorAuthResp().resp_update()
