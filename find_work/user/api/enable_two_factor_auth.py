from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from user.models import User

from util.success_resp_data import UpdateSuccess
from util.error_resp_data import TwoFactorAuthAlreadyEnabledError


class EnableTwoFactorAuth(APIView):
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
            return Response(
                status=TwoFactorAuthAlreadyEnabledError().get_status(),
                data=TwoFactorAuthAlreadyEnabledError().get_data()
            )

        user.is_two_factor_auth = True
        user.save()

        return Response(
            status=UpdateSuccess().get_status(),
            data=UpdateSuccess().get_data()
        )
