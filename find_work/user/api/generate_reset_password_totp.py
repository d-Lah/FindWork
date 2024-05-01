import pyotp

from rest_framework.views import APIView
from rest_framework.response import Response

from cryptography.fernet import Fernet

from find_work.settings import CRYPTOGRAPHY_FERNET_KEY

from user.models import User
from user.serializer import GenerateResetPasswordTOTPSerializer

from util import success_resp_data
from util.mail_sender import MailSender
from util.mail_data_manager import (
    MailSubjectInGenerateResetPasswordUuid,
    MailMessageInGenerateResetPasswordUuid,
)


class GenerateResetPasswordTOTP(APIView):
    def post(
            self,
            request
    ):
        serializer = GenerateResetPasswordTOTPSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

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
            status=success_resp_data.create["status_code"],
            data=success_resp_data.create["data"]
        )
