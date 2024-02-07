from django.contrib.auth.hashers import check_password

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from user.models import User
from user.serializer import ValidatePasswordSerializer

from util.error_resp_data import (
    FieldsEmptyError,
    WrongPasswordError,
)
from util.success_resp_data import ValidateSuccess


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
            return Response(
                status=FieldsEmptyError().get_status(),
                data=FieldsEmptyError().get_data()
            )

        user_id = request.user.id
        user = User.objects.filter(pk=user_id).first()

        serialized_data = serializer.validated_data

        is_check_password = check_password(
            serialized_data["password"],
            user.password
        )
        if not is_check_password:
            return Response(
                status=WrongPasswordError().get_status(),
                data=WrongPasswordError().get_data()
            )

        return Response(
            status=ValidateSuccess().get_status(),
            data=ValidateSuccess().get_data()
        )
