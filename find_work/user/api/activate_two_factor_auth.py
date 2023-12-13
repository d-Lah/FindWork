from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from user.models import User

from apps.response_success import ResponseUpdate
from apps.response_error import ResponseTwoFactorAuthAlreadyActiveError


class ActivateTwoFactorAuth(APIView):
    """API change is_two_factor_auth on true"""

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
            return ResponseTwoFactorAuthAlreadyActiveError().get_response()

        user.is_two_factor_auth = True
        user.save()

        return ResponseUpdate().get_response()
