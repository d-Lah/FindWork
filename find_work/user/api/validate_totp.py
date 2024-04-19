import pyotp

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from cryptography.fernet import Fernet

from find_work.settings import CRYPTOGRAPHY_FERNET_KEY

from user.models import User
from user.serializer import ValidateTOTPSerializer

from util import error_resp_data
from util import success_resp_data
from util.exceptions import TOTPIncapException


class ValidateTOTP(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(
            self,
            request
    ):
        user_id = request.user.id

        serializer = ValidateTOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serialized_data = serializer.validated_data

        user = User.objects.filter(pk=user_id).first()

        fernet = Fernet(CRYPTOGRAPHY_FERNET_KEY.encode())
        user_otp_base32 = fernet.decrypt(user.otp_base32)

        totp = pyotp.TOTP(user_otp_base32)
        if not totp.verify(serialized_data["totp"]):
            raise TOTPIncapException(error_resp_data.totp_incap)

        if not user.is_two_factor_auth:
            user.is_two_factor_auth = True
            user.save()

        return Response(
            status=success_resp_data.validate["status_code"],
            data=success_resp_data.validate["data"]
        )
