from django.contrib.auth.hashers import check_password

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from user.models import User
from user.serializer import PasswordFieldSerializer

from apps.response_error import (
    ResponseWrongPasswordError,
    ResponsePasswordFieldEmptyError,
)
from apps.response_success import ResponseValid


class CheckUserPassword(APIView):
    """API validate password"""

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(
            self,
            request
    ):
        password_serializer = PasswordFieldSerializer(data=request.data)
        password_serializer.is_valid()

        deserialized_data = password_serializer.validated_data

        if password_serializer.errors:
            return ResponsePasswordFieldEmptyError().get_response()

        user_id = request.user.id
        user = User.objects.filter(pk=user_id).first()

        is_check_password = check_password(
            deserialized_data["password"],
            user.password
        )
        if not is_check_password:
            return ResponseWrongPasswordError().get_response()

        return ResponseValid().get_response()
