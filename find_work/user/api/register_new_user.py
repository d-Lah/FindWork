import pyotp

from uuid import uuid4

from django.urls import reverse
from django.contrib.auth.hashers import make_password

from rest_framework.views import APIView

from cryptography.fernet import Fernet

from find_work.settings import HTTP_LOCALHOST
from find_work.settings import CRYPTOGRAPHY_FERNET_KEY

from user.models import (
    User,
    Profile,
)
from user.serializer import RegisterNewUserSerializer

from util.mail_data_manager import (
    MailSubjectInRegisterNewUser,
    MailMessageInRegisterNewUser,
)
from util.mail_sender import MailSender
from util.user_api_resp.register_new_user_resp import RegisterNewUserResp


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


def is_email_already_exists(errors):
    if not errors.get("email"):
        return False

    if errors["email"][0] == "This field must be unique.":
        return True

    return False


class RegisterNewUser(APIView):
    def post(
            self,
            request,
    ):
        serializer = RegisterNewUserSerializer(data=request.data)

        serializer.is_valid()

        if is_fields_empty(serializer.errors):
            return RegisterNewUserResp().resp_fields_empty_error()

        if is_invalid_email(serializer.errors):
            return RegisterNewUserResp().resp_invalid_email_address_error()

        if is_email_already_exists(serializer.errors):
            return RegisterNewUserResp().resp_fields_already_exists_error(
                serializer.errors
            )

        serializer_data = serializer.validated_data

        new_profile = Profile(
            first_name=serializer_data["first_name"],
            last_name=serializer_data["last_name"],
        )
        new_profile.save()

        fernet = Fernet(CRYPTOGRAPHY_FERNET_KEY.encode())
        user_otp_base32 = pyotp.random_base32()
        user_encrypted_opt_base32 = fernet.encrypt(user_otp_base32.encode())

        new_user = User(
            email=serializer_data["email"],
            user_activation_uuid=uuid4(),
            profile=new_profile,
            is_employer=serializer_data["is_employer"],
            is_employee=serializer_data["is_employee"],
            password=make_password(serializer_data["password"]),
            otp_base32=user_encrypted_opt_base32.decode()
        )
        new_user.save()

        new_user_activation_uuid = new_user.user_activation_uuid
        activate_user_kwargs = {
            "user_activation_uuid": new_user_activation_uuid
        }
        activate_user_view_url = reverse(
            "user_api:activate_new_user",
            kwargs=activate_user_kwargs
        )

        link_on_activate_new_user = HTTP_LOCALHOST + activate_user_view_url
        mail_subject = MailSubjectInRegisterNewUser().get_mail_subject()
        mail_message = MailMessageInRegisterNewUser(
            link_on_activate_new_user
        ).get_mail_message()

        MailSender(
            mail_subject=mail_subject,
            mail_message=mail_message,
            for_user=new_user.email
        ).send_mail_to_user()

        return RegisterNewUserResp().resp_create()
