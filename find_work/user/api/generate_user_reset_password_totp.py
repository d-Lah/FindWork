import pyotp

from rest_framework.views import APIView

from cryptography.fernet import Fernet

from find_work.settings import CRYPTOGRAPHY_FERNET_KEY

from user.models import User
from user.serializer import EmailFieldSerializer

from apps.response_error import (
    ResponseUserNotFoundError,
    ResponseEmailFieldEmptyError,
)
from apps.mail_sender import MailSender
from apps.mail_data_manager import (
    MailSubjectInGenerateResetPasswordUuid,
    MailMessageInGenerateResetPasswordUuid,
)
from apps.response_success import ResponseCreate


class GenerateUserResetPasswordTOTP(APIView):
    def post(
            self,
            request
    ):
        email_serializer = EmailFieldSerializer(data=request.data)

        email_serializer.is_valid()
        if email_serializer.errors:
            return ResponseEmailFieldEmptyError().get_response()

        deserialized_data = email_serializer.validated_data

        user = User.objects.filter(email=deserialized_data["email"]).first()

        if not user:
            return ResponseUserNotFoundError().get_response()

        fernet = Fernet(CRYPTOGRAPHY_FERNET_KEY.encode())
        user_otp_base32 = fernet.decrypt(user.otp_base32.encode())

        totp = pyotp.TOTP(
            s=user_otp_base32,
            interval=172880
        )
        reset_password_totp = totp.now()

        mail_subject = MailSubjectInGenerateResetPasswordUuid().get_mail_subject()
        mail_message = MailMessageInGenerateResetPasswordUuid(
            reset_password_totp
        ).get_mail_message()

        MailSender(
            mail_subject=mail_subject,
            mail_message=mail_message,
            for_user=user.email
        ).send_mail_to_user()

        return ResponseCreate().get_response()
