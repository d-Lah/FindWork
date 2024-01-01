import pyotp

from rest_framework.views import APIView

from cryptography.fernet import Fernet

from find_work.settings import CRYPTOGRAPHY_FERNET_KEY

from user.models import User
from user.serializer import (
    ValidateResetPasswordTOTPSerializer
)

from util.user_api_resp.validate_reset_password_totp_resp import (
    ValidateResetPasswordTOTPResp
)


def is_fields_empty(errors):
    if not errors:
        return False

    for field in errors:
        if "blank" in errors[field][0]:
            return True

    return False


def is_invalid_email(errors):
    if not errors.get("email"):
        return False

    if "valid email address" in errors["email"][0]:
        return True

    return False


def is_user_not_found(errors):
    if not errors.get("email"):
        return False

    if errors["email"][0] == "User with given email not found":
        return True

    return False


class ValidateResetPasswordTOTP(APIView):
    def post(
            self,
            request
    ):
        serializer = ValidateResetPasswordTOTPSerializer(
            data=request.data
        )

        serializer.is_valid()

        if is_fields_empty(serializer.errors):
            return ValidateResetPasswordTOTPResp().resp_fields_empty_error()

        if is_invalid_email(serializer.errors):
            return ValidateResetPasswordTOTPResp(
            ).resp_invalid_email_address_error()

        if is_user_not_found(serializer.errors):
            return ValidateResetPasswordTOTPResp().resp_user_not_found_error()

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
            return ValidateResetPasswordTOTPResp(
            ).resp_reset_password_totp_incap_error()

        return ValidateResetPasswordTOTPResp().resp_valid()
