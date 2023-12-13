from rest_framework.views import APIView

from user.models import User

from apps.response_success import ResponseUpdate
from apps.response_error import ResponseUserAlreadyActiveError


class ActivateUser(APIView):
    """API class for activate new user"""

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
            return ResponseUserAlreadyActiveError().get_response()

        user.is_active = True
        user.save()
        return ResponseUpdate().get_response()
