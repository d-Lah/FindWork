import pyotp

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from cryptography.fernet import Fernet

from find_work.settings import CRYPTOGRAPHY_FERNET_KEY

from user.models import User

from util.user_api_resp.get_two_factor_auth_qr_code_resp import (
    GetTwoFacteorAuthQRCodeResp
)


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

        return GetTwoFacteorAuthQRCodeResp().resp_get(otp_auth_url)
