import pyotp

from uuid import uuid4

from django.urls import reverse
from django.contrib.auth.hashers import make_password

from rest_framework.views import APIView
from rest_framework.response import Response

from cryptography.fernet import Fernet

from find_work.settings import HTTP_LOCALHOST
from find_work.settings import CRYPTOGRAPHY_FERNET_KEY

from user.models import (
    User,
    Profile,
)
from user.serializer import RegisterNewUserSerializer

from util.error_resp_data import (
    FieldsEmptyError,
    EmailAlreadyExistsError,
    InvalidEmailAdressError,
)
from util.error_exceptions import (
    IsFieldsEmpty,
    IsFieldsInvalid,
    IsFieldsAlreadyExists,
)
from util.mail_data_manager import (
    MailSubjectInRegisterNewUser,
    MailMessageInRegisterNewUser,
)
from util.mail_sender import MailSender
from util.success_resp_data import CreateSuccess
from util.error_validation import ErrorValidation


class RegisterNewUser(APIView):
    def post(
            self,
            request,
    ):
        serializer = RegisterNewUserSerializer(data=request.data)

        serializer.is_valid()

        error_validation = ErrorValidation(serializer.errors)
        try:
            error_validation.is_fields_empty()
            error_validation.is_fields_invalid()
            error_validation.is_fields_already_exists()
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
        except IsFieldsAlreadyExists:
            return Response(
                status=EmailAlreadyExistsError().get_status(),
                data=EmailAlreadyExistsError().get_data()
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

        return Response(
            status=CreateSuccess().get_status(),
            data=CreateSuccess().get_data()
        )
