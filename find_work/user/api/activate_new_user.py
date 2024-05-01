from rest_framework.views import APIView
from rest_framework.response import Response

from user.models import User

from util import error_resp_data
from util.exceptions import UserActivationUUIDIncapException
from util import success_resp_data


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
            raise UserActivationUUIDIncapException(
                error_resp_data.user_activation_uuid_incap
            )

        user.is_active = True
        user.save()
        return Response(
            status=success_resp_data.update["status_code"],
            data=success_resp_data.update["data"]
        )
