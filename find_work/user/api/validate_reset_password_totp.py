import pyotp

from rest_framework.views import APIView
from rest_framework.response import Response

from cryptography.fernet import Fernet

from find_work.settings import CRYPTOGRAPHY_FERNET_KEY

from user.models import User
from user.serializer import (
    ValidateResetPasswordTOTPSerializer
)

from util.error_resp_data import (
    FieldsEmptyError,
    UserNotFoundError,
    InvalidEmailAdressError,
    ResetPasswordTOTPIncapError
)
from util.error_exceptions import (
    IsFieldsEmpty,
    IsFieldsInvalid,
    IsFieldsNotFound
)
from util.error_validation import ErrorValidation
from util.success_resp_data import ValidateSuccess


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

    if errors["email"][0] == "User not found":
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

        error_validation = ErrorValidation(serializer.errors)
        try:
            error_validation.is_fields_empty()
            error_validation.is_fields_invalid()
            error_validation.is_fields_not_found()
        except IsFieldsEmpty:
            return Response(
                status=FieldsEmptyError().get_status(),
                data=FieldsEmptyError().get_data()
            )
        except IsFieldsInvalid:
            return Response(
                status=InvalidEmailAdressError().get_status(),
                data=InvalidEmailAdressError().get_data()
            )
        except IsFieldsNotFound:
            return Response(
                status=UserNotFoundError().get_status(),
                data=UserNotFoundError().get_data()
            )

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
            return Response(
                status=ResetPasswordTOTPIncapError().get_status(),
                data=ResetPasswordTOTPIncapError().get_data()
            )

        return Response(
            status=ValidateSuccess().get_status(),
            data=ValidateSuccess().get_data()
        )
