import pyotp

from uuid import uuid4

from django.urls import reverse
from django.contrib.auth.hashers import make_password

from rest_framework.views import APIView

from cryptography.fernet import Fernet

from find_work.settings import CRYPTOGRAPHY_FERNET_KEY

from user.models import (
    User,
    Profile,
    EmployerProfile,
    EmployeeProfile,
)
from user.serializer import (
    UserSerializer,
    ProfileSerializer,
)

from apps.object_exception import (
    EmailAlreadyExistsError,
    PhoneNuberAlreadyExistsError,
)
from apps.response_success import (
    ResponseCreate,
)
from apps.mail_data_manager import (
    MailSubjectInRegisterNewUser,
    MailMessageInRegisterNewUser,
)
from apps.mail_sender import MailSender
from apps.response_error import (
    ResponseUserFieldEmptyError,
    ResponseProfileFieldEmptyError,
    ResponseEmailAlreadyExistsError,
    ResponsePhoneNumberAlreadyExistsError,
)
from find_work.settings import HTTP_LOCALHOST

from user.apps_for_user.user_data_validators import (
    ValidateEmailAndPhoneNumberOnExists
)


class RegisterNewUser(APIView):
    """Class for register new user"""

    def post(
            self,
            request,
    ):
        user_serializer = UserSerializer(data=request.data)
        user_serializer.is_valid()

        deserialized_user_data = user_serializer.validated_data

        user_data_validators = ValidateEmailAndPhoneNumberOnExists(
            deserialized_user_data.get("email"),
            deserialized_user_data.get("phone_number"),
        )

        try:
            user_data_validators.is_email_exists()
            user_data_validators.is_phone_number_exists()

        except EmailAlreadyExistsError:
            return ResponseEmailAlreadyExistsError().get_response()

        except PhoneNuberAlreadyExistsError:
            return ResponsePhoneNumberAlreadyExistsError().get_response()

        if user_serializer.errors:
            return ResponseUserFieldEmptyError().get_response()

        profile_serializer = ProfileSerializer(data=request.data)
        profile_serializer.is_valid()

        if profile_serializer.errors:
            return ResponseProfileFieldEmptyError().get_response()

        deserialized_profile_data = profile_serializer.validated_data

        if deserialized_user_data.get("is_employer"):
            new_employer_profile = EmployerProfile()
            new_employer_profile.save()
        else:
            new_employer_profile = None

        if deserialized_user_data.get("is_employee"):
            new_employee_profile = EmployeeProfile()
            new_employee_profile.save()
        else:
            new_employee_profile = None

        new_profile = Profile(
            first_name=deserialized_profile_data["first_name"],
            second_name=deserialized_profile_data["second_name"],
            employer_profile=new_employer_profile,
            employee_profile=new_employee_profile,
        )
        new_profile.save()

        fernet = Fernet(CRYPTOGRAPHY_FERNET_KEY.encode())
        user_otp_base32 = pyotp.random_base32()
        user_encrypted_opt_base32 = fernet.encrypt(user_otp_base32.encode())

        new_user = User(
            email=deserialized_user_data["email"],
            phone_number=deserialized_user_data["phone_number"],
            user_activation_uuid=uuid4(),
            profile=new_profile,
            is_employer=deserialized_user_data["is_employer"],
            is_employee=deserialized_user_data["is_employee"],
            password=make_password(deserialized_user_data["password"]),
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
        return ResponseCreate().get_response()
