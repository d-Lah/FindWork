from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from user.models import User

from util.user_api_resp.deactivate_two_factor_auth_resp import (
    DeactivateTwoFactorAuthResp
)


class DeactivateTwoFactorAuth(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(
            self,
            request
    ):
        user_id = request.user.id

        user = User.objects.filter(
            pk=user_id,
            is_two_factor_auth=True
        ).first()

        if not user:
            return DeactivateTwoFactorAuthResp(
            ).resp_two_factor_auth_already_deactivated_error()

        user.is_two_factor_auth = False
        user.save()

        return DeactivateTwoFactorAuthResp().resp_update()
