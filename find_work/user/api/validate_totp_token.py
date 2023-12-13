import pyotp

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from cryptography.fernet import Fernet

from find_work.settings import CRYPTOGRAPHY_FERNET_KEY

from user.models import User
from user.serializer import TOTPTokenSerializer

from apps.response_error import (
    ResponseWrongTOTPTokenError,
    ResponseTOTPTokenFieldEmptyError,
)
from apps.response_success import ResponseValid


class ValidateTOTPToken(APIView):
    """API class for validation totp token from authenticator app"""

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(
            self,
            request
    ):
        user_id = request.user.id

        totp_token_serializer = TOTPTokenSerializer(data=request.data)
        totp_token_serializer.is_valid()

        if totp_token_serializer.errors:
            return ResponseTOTPTokenFieldEmptyError().get_response()

        deserialized_data = totp_token_serializer.validated_data

        user = User.objects.filter(pk=user_id).first()

        fernet = Fernet(CRYPTOGRAPHY_FERNET_KEY.encode())
        user_otp_base32 = fernet.decrypt(user.otp_base32)

        totp = pyotp.TOTP(user_otp_base32)
        if not totp.verify(deserialized_data["totp_token"]):
            return ResponseWrongTOTPTokenError().get_response()

        if not user.is_two_factor_auth:
            user.is_two_factor_auth = True
            user.save()

        return ResponseValid().get_response()
