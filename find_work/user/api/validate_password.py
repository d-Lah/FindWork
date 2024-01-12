from django.contrib.auth.hashers import check_password

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from user.models import User
from user.serializer import ValidatePasswordSerializer

from util.user_api_resp.validate_password_resp import (
    ValidatePasswordResp
)


class ValidatePassword(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(
            self,
            request
    ):
        serializer = ValidatePasswordSerializer(data=request.data)
        serializer.is_valid()

        if serializer.errors:
            return ValidatePasswordResp().resp_fields_empty_error()

        user_id = request.user.id
        user = User.objects.filter(pk=user_id).first()

        serialized_data = serializer.validated_data

        is_check_password = check_password(
            serialized_data["password"],
            user.password
        )
        if not is_check_password:
            return ValidatePasswordResp().resp_wrong_password_error()

        return ValidatePasswordResp().resp_valid()
