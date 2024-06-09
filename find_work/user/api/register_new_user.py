import pyotp

from uuid import uuid4

from django.urls import reverse
from django.contrib.auth.hashers import make_password

from rest_framework.views import APIView
from rest_framework.response import Response

from cryptography.fernet import Fernet

from find_work.settings import HTTP_LOCALHOST_REACT, CRYPTOGRAPHY_FERNET_KEY

from user.models import (
    User,
    Profile,
)
from user.serializer import RegisterNewUserSerializer

from util import success_resp_data
from util.mail_data_manager import (
    MailSubjectInRegisterNewUser,
    MailMessageInRegisterNewUser,
)
from util.mail_sender import MailSender


class RegisterNewUser(APIView):
    def post(
        self,
        request,
    ):
        serializer = RegisterNewUserSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer_data = serializer.validated_data

        new_profile = Profile.objects.create(
            first_name=serializer_data["first_name"],
            last_name=serializer_data["last_name"],
        )

        fernet = Fernet(CRYPTOGRAPHY_FERNET_KEY.encode())
        user_otp_base32 = pyotp.random_base32()
        user_encrypted_opt_base32 = fernet.encrypt(user_otp_base32.encode())

        new_user = User.objects.create(
            email=serializer_data["email"],
            user_activation_uuid=uuid4(),
            profile=new_profile,
            is_employer=serializer_data["is_employer"],
            is_employee=serializer_data["is_employee"],
            password=make_password(serializer_data["password"]),
            otp_base32=user_encrypted_opt_base32.decode(),
        )
        new_user.save()

        activation_uuid = new_user.user_activation_uuid
        activate_user_view_url = f"/activate-user/{activation_uuid}"

        link_on_activate_new_user = (
            HTTP_LOCALHOST_REACT + activate_user_view_url
        )
        mail_subject = MailSubjectInRegisterNewUser().get_mail_subject()
        mail_message = MailMessageInRegisterNewUser(
            link_on_activate_new_user
        ).get_mail_message()

        MailSender(
            mail_subject=mail_subject,
            mail_message=mail_message,
            for_user=new_user.email,
        ).send_mail_to_user()

        return Response(
            status=success_resp_data.create["status_code"],
            data=success_resp_data.create["data"],
        )
