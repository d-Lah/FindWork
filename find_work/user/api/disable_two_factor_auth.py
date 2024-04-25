from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response

from user.models import User

from util import error_resp_data
from util import success_resp_data
from util.exceptions import AlreadyEnableOrDisableException


class DisableTwoFactorAuth(APIView):
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
            raise AlreadyEnableOrDisableException(
                error_resp_data.already_disable
            )

        user.is_two_factor_auth = False
        user.save()

        return Response(
            status=success_resp_data.update["status_code"],
            data=success_resp_data.update["data"]
        )
