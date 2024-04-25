import pyotp

from rest_framework.views import APIView
from rest_framework.response import Response

from cryptography.fernet import Fernet

from find_work.settings import CRYPTOGRAPHY_FERNET_KEY

from user.models import User
from user.serializer import (
    ValidateResetPasswordTOTPSerializer
)

from util import error_resp_data
from util import success_resp_data
from util.exceptions import TOTPIncapException


class ValidateResetPasswordTOTP(APIView):
    def post(
            self,
            request
    ):
        serializer = ValidateResetPasswordTOTPSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        serializer_data = serializer.validated_data

        user = User.objects.filter(email=serializer_data["email"]).first()

        fernet = Fernet(CRYPTOGRAPHY_FERNET_KEY.encode())
        user_otp_base32 = fernet.decrypt(user.otp_base32.encode())

        totp = pyotp.TOTP(
            s=user_otp_base32.decode(),
            interval=172880
        )
        if not totp.verify(
            serializer_data["reset_password_totp"]
        ):
            raise TOTPIncapException(error_resp_data.reset_password_totp_incap)

        return Response(
            status=success_resp_data.validate["status_code"],
            data=success_resp_data.validate["data"]
        )
