from rest_framework.views import APIView
from rest_framework.response import Response

from user.models import User

from util.success_resp_data import UpdateSuccess
from util.error_resp_data import UserActivateUUIDIncapError


class ActivateNewUser(APIView):
    def put(
            self,
            request,
            user_activation_uuid,
    ):
        user = User.objects.filter(
            user_activation_uuid=user_activation_uuid,
            is_active=False,
        ).first()

        if not user:
            return Response(
                status=UserActivateUUIDIncapError().get_status(),
                data=UserActivateUUIDIncapError().get_data()
            )

        user.is_active = True
        user.save()
        return Response(
            status=UpdateSuccess().get_status(),
            data=UpdateSuccess().get_data()
        )
