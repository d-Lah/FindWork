from rest_framework.views import APIView

from user.models import User

from util.user_api_resp.activate_new_user_resp import ActivateNewUserResp


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
            return ActivateNewUserResp().resp_user_already_active_error()

        user.is_active = True
        user.save()
        return ActivateNewUserResp().resp_update()
