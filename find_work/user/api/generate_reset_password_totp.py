import pyotp

from rest_framework.views import APIView
from rest_framework.response import Response

from cryptography.fernet import Fernet

from find_work.settings import CRYPTOGRAPHY_FERNET_KEY

from user.models import User
from user.serializer import GenerateResetPasswordTOTPSerializer

from util.error_resp_data import (
    FieldsEmptyError,
    UserNotFoundError,
    InvalidEmailAdressError,
)
from util.mail_sender import MailSender
from util.mail_data_manager import (
    MailSubjectInGenerateResetPasswordUuid,
    MailMessageInGenerateResetPasswordUuid,
)
from util.success_resp_data import CreateSuccess


def is_fields_empty(errors):
    if not errors:
        return False

    if "blank" in errors["email"][0]:
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


class GenerateResetPasswordTOTP(APIView):
    def post(
            self,
            request
    ):
        serializer = GenerateResetPasswordTOTPSerializer(
            data=request.data
        )

        serializer.is_valid()

        if is_fields_empty(serializer.errors):
            return Response(
                status=FieldsEmptyError().get_status(),
                data=FieldsEmptyError().get_data()
            )

        if is_invalid_email(serializer.errors):
            return Response(
                status=InvalidEmailAdressError().get_status(),
                data=InvalidEmailAdressError().get_data()
            )

        if is_user_not_found(serializer.errors):
            return Response(
                status=UserNotFoundError().get_status(),
                data=UserNotFoundError().get_data()
            )

        serializer_data = serializer.validated_data

        user = User.objects.filter(email=serializer_data["email"]).first()

        fernet = Fernet(CRYPTOGRAPHY_FERNET_KEY.encode())
        user_otp_base32 = fernet.decrypt(user.otp_base32.encode())

        totp = pyotp.TOTP(
            s=user_otp_base32,
            interval=172880
        )
        reset_password_totp = totp.now()

        mail_subject = MailSubjectInGenerateResetPasswordUuid(
        ).get_mail_subject()
        mail_message = MailMessageInGenerateResetPasswordUuid(
            reset_password_totp
        ).get_mail_message()

        MailSender(
            mail_subject=mail_subject,
            mail_message=mail_message,
            for_user=user.email
        ).send_mail_to_user()

        return Response(
            status=CreateSuccess().get_status(),
            data=CreateSuccess().get_data()
        )
