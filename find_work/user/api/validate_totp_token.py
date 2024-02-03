import pyotp

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from cryptography.fernet import Fernet

from find_work.settings import CRYPTOGRAPHY_FERNET_KEY

from user.models import User
from user.serializer import ValidateTOTPTokenSerializer

from util.error_resp_data import (
    FieldsEmptyError,
    WrongTOTPTokenError
)
from util.success_resp_data import ValidateSuccess


class ValidateTOTPToken(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(
            self,
            request
    ):
        user_id = request.user.id

        serializer = ValidateTOTPTokenSerializer(data=request.data)
        serializer.is_valid()

        if serializer.errors:
            return Response(
                status=FieldsEmptyError().get_status(),
                data=FieldsEmptyError().get_data()
            )

        serialized_data = serializer.validated_data

        user = User.objects.filter(pk=user_id).first()

        fernet = Fernet(CRYPTOGRAPHY_FERNET_KEY.encode())
        user_otp_base32 = fernet.decrypt(user.otp_base32)

        totp = pyotp.TOTP(user_otp_base32)
        if not totp.verify(serialized_data["totp_token"]):
            return Response(
                status=WrongTOTPTokenError().get_status(),
                data=WrongTOTPTokenError().get_data()
            )

        if not user.is_two_factor_auth:
            user.is_two_factor_auth = True
            user.save()

        return Response(
            status=ValidateSuccess().get_status(),
            data=ValidateSuccess().get_data()
        )
