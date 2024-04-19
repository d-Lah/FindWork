import pyotp

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from cryptography.fernet import Fernet

from find_work.settings import CRYPTOGRAPHY_FERNET_KEY

from user.models import User

from util import success_resp_data


class GetTwoFactorAuthQRCode(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(
            self,
            request
    ):
        user_id = request.user.id
        user = User.objects.filter(pk=user_id).first()

        fernet = Fernet(CRYPTOGRAPHY_FERNET_KEY.encode())
        user_otp_base32 = fernet.decrypt(user.otp_base32.encode())

        otp_auth_url = pyotp.TOTP(
            user_otp_base32.decode()
        ).provisioning_uri(
            name=user.email,
            issuer_name="FindWork"
        )

        resp_data = success_resp_data.get["data"]
        resp_data["request_data"] = otp_auth_url

        return Response(
            status=success_resp_data.get["status_code"],
            data=resp_data
        )
