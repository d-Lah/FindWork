import pyotp

from rest_framework.views import APIView

from cryptography.fernet import Fernet

from find_work.settings import CRYPTOGRAPHY_FERNET_KEY

from user.models import User

from user.serializer import (
    EmailFieldSerializer,
    ResetPasswordTOTPSerializer,
)

from apps.response_success import ResponseValid
from apps.response_error import (
    ResponseUserNotFoundError,
    ResponseEmailFieldEmptyError,
    ResponseTOTPTokenFieldEmptyError,
    ResponseResetPasswordTOTPIncapacitatedError,
)
from apps.fields_validators import ValidateFieldsOnEmpty
from apps.object_exception import (
    EmailFieldEmptyError,
    ResetPasswordPasswordTOTPFieldEmptyError,
)


class ValidateUserResetPasswordTOTP(APIView):
    def post(
            self,
            request
    ):
        email_serializer = EmailFieldSerializer(data=request.data)
        reset_password_totp_serializer = ResetPasswordTOTPSerializer(
            data=request.data
        )

        email_serializer.is_valid()
        reset_password_totp_serializer.is_valid()

        validate_field = {
            "email": email_serializer.errors,
            "reset_password_totp": reset_password_totp_serializer.errors
        }

        data_validators = ValidateFieldsOnEmpty(
            validate_field
        )

        try:
            data_validators.is_email_field_empty()
            data_validators.is_reset_password_totp_field_empty()

        except EmailFieldEmptyError:
            return ResponseEmailFieldEmptyError().get_response()

        except ResetPasswordPasswordTOTPFieldEmptyError:
            return ResponseTOTPTokenFieldEmptyError().get_response()

        email_serializer_data = email_serializer.validated_data
        user = User.objects.filter(
            email=email_serializer_data["email"]
        ).first()

        if not user:
            return ResponseUserNotFoundError().get_response()

        fernet = Fernet(CRYPTOGRAPHY_FERNET_KEY.encode())
        user_otp_base32 = fernet.decrypt(user.otp_base32.encode())

        reset_password_totp_serializer_data = (
            reset_password_totp_serializer.validated_data
        )

        totp = pyotp.TOTP(
            s=user_otp_base32.decode(),
            interval=172880
        )
        if not totp.verify(
            reset_password_totp_serializer_data["reset_password_totp"]
        ):
            return ResponseResetPasswordTOTPIncapacitatedError().get_response()

        return ResponseValid().get_response()
