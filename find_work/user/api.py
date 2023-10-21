from uuid import uuid4

import pyotp

from django.urls import reverse
from django.contrib.auth.hashers import (
    make_password,
    check_password,
)

from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import (
    User,
    Profile,
    EmployerProfile,
    EmployeeProfile,
)
from .serializer import (
    UserSerializer,
    ProfileSerializer,
    TOTPTokenSerializer,
    UserAvatarSerializer,
    EmailFieldSerializer,
    PhoneNumberFieldSerializer,
    PasswordFieldSerializer,
    EmployerProfileSerializer,
    EmployeeProfileSerializer,
)
from find_work.settings import (
    HTTP_LOCALHOST,
    ALLOWED_FILE_EXT,
    FILE_UPLOAD_MAX_MEMORY_SIZE,
)
from apps.object_exception import (
    EmailAlreadyExistsError,
    PhoneNuberAlreadyExistsError
)
from apps.response_success import (
    ResponseGet,
    ResponseValid,
    ResponseCreate,
    ResponseUpdate,
)
from apps.mail_data_manager import (
    MailSubjectInRegisterNewUser,
    MailMessageInRegisterNewUser
)
from apps.mail_sender import MailSender
from apps.response_error import (
    ResponseWrongPasswordError,
    ResponseWrongTOTPTokenError,
    ResponseUserFieldEmptyError,
    ResponseEmailFieldEmptyError,
    ResponseProfileFieldEmptyError,
    ResponseUserAlreadyActiveError,
    ResponseEmailAlreadyExistsError,
    ResponsePasswordFieldEmptyError,
    ResponseTOTPTokenFieldEmptyError,
    ResponsePhoneNumberFieldEmptyError,
    ResponsePhoneNumberAlreadyExistsError,
    ResponseTwoFactorAuthAlreadyActiveError,
)
from .apps_for_user.user_data_validators import (
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

        new_user = User(
            email=deserialized_user_data["email"],
            phone_number=deserialized_user_data["phone_number"],
            user_activation_uuid=uuid4(),
            profile=new_profile,
            is_employer=deserialized_user_data["is_employer"],
            is_employee=deserialized_user_data["is_employee"],
            password=make_password(deserialized_user_data["password"]),
        )
        new_user.save()

        new_user_activation_uuid = new_user.user_activation_uuid
        activate_user_kwargs = {
            "user_activation_uuid": new_user_activation_uuid
        }
        activate_user_view_url = reverse(
            "user_api:activate_user",
            kwargs=activate_user_kwargs
        )

        link_on_activate_new_user = HTTP_LOCALHOST + activate_user_view_url
        mail_subject = MailSubjectInRegisterNewUser().get_mail_subject()
        mail_message = MailMessageInRegisterNewUser(
            new_profile.first_name,
            link_on_activate_new_user
        ).get_mail_message()

        MailSender(
            mail_subject=mail_subject,
            mail_message=mail_message,
            for_user=new_user.email
        ).send_mail_to_user()
        return ResponseCreate().get_response()


class ActivateUser(APIView):
    """API class for activate new user"""

    def put(
            self,
            request,
            user_activation_uuid,
    ):
        user = User.objects.filter(
            user_activation_uuid=user_activation_uuid,
            is_active=False,
        ).first()

        if not user:
            return ResponseUserAlreadyActiveError().get_response()

        user.is_active = True
        user.save()
        return ResponseUpdate().get_response()


class CreateTwoFactorAuthQRCode(APIView):
    """API class for create base32 and qr code for authenticator app"""

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(
            self,
            request
    ):
        user_id = request.user.id
        user = User.objects.filter(pk=user_id).first()

        otp_base32 = pyotp.random_base32()
        otp_auth_url = pyotp.TOTP(
            otp_base32
        ).provisioning_uri(
            name=user.email,
            issuer_name="FindWork"
        )

        user.otp_base32 = otp_base32
        user.save()

        response_data = ResponseCreate()
        response_data.add_data_for_response_data(
            "otp_auth_url",
            otp_auth_url
        )

        return response_data.get_response()


class ValidateTOTPToken(APIView):
    """API class for validation totp token from authenticator app"""

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(
            self,
            request
    ):
        user_id = request.user.id

        totp_token_serializer = TOTPTokenSerializer(data=request.data)
        totp_token_serializer.is_valid()

        if totp_token_serializer.errors:
            return ResponseTOTPTokenFieldEmptyError().get_response()

        deserialized_data = totp_token_serializer.validated_data

        user = User.objects.filter(pk=user_id).first()

        user_otp_base32 = user.otp_base32

        totp = pyotp.TOTP(user_otp_base32)
        if not totp.verify(deserialized_data["totp_token"]):
            return ResponseWrongTOTPTokenError().get_response()

        if not user.is_two_factor_auth:
            user.is_two_factor_auth = True
            user.save()

        return ResponseValid().get_response()


class ActivateTwoFactorAuth(APIView):
    """API change is_two_factor_auth on true"""

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(
            self,
            request
    ):
        user_id = request.user.id

        user = User.objects.filter(
            pk=user_id,
            is_two_factor_auth=False
        ).first()

        if not user:
            return ResponseTwoFactorAuthAlreadyActiveError().get_response()

        user.is_two_factor_auth = True
        user.save()

        return ResponseUpdate().get_response()


class UserInfo(APIView):
    """API should response data with some user data to show them"""

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(
            self,
            request
    ):
        user_id = request.user.id
        user = User.objects.filter(pk=user_id).first()

        user_serializer = UserSerializer(user)
        profile_serializer = ProfileSerializer(user.profile)

        serialized_user_data = user_serializer.data
        serialized_profile_data = profile_serializer.data

        response_data = ResponseGet()
        response_data.add_data_for_response_data(
            "user_data",
            serialized_user_data
        )
        response_data.add_data_for_response_data(
            "profile_data",
            serialized_profile_data
        )
        return response_data.get_response()


class EditProfileInfo(APIView):
    """API will edit first name and second name"""

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(
            self,
            request
    ):
        profile_serializer = ProfileSerializer(data=request.data)

        profile_serializer.is_valid()
        if profile_serializer.errors:
            return ResponseProfileFieldEmptyError().get_response()

        user_id = request.user.id
        profile = Profile.objects.filter(user__id=user_id).first()

        deserialized_data = profile_serializer.validated_data

        profile.first_name = deserialized_data["first_name"]
        profile.second_name = deserialized_data["second_name"]

        profile.save()

        return ResponseUpdate().get_response()


class CheckUserPassword(APIView):
    """API validate password"""

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(
            self,
            request
    ):
        password_serializer = PasswordFieldSerializer(data=request.data)
        password_serializer.is_valid()

        deserialized_data = password_serializer.validated_data

        if password_serializer.errors:
            return ResponsePasswordFieldEmptyError().get_response()

        user_id = request.user.id
        user = User.objects.filter(pk=user_id).first()

        is_check_password = check_password(
            deserialized_data["password"],
            user.password
        )
        if not is_check_password:
            return ResponseWrongPasswordError().get_response()

        return ResponseValid().get_response()


class UpdateUserPassword(APIView):
    "API update password"

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(
            self,
            request
    ):
        password_serializer = PasswordFieldSerializer(data=request.data)
        password_serializer.is_valid()

        deserialized_data = password_serializer.validated_data

        if password_serializer.errors:
            return ResponsePasswordFieldEmptyError().get_response()

        user_id = request.user.id
        user = User.objects.filter(pk=user_id).first()

        user.password = make_password(deserialized_data["password"])
        user.save()

        return ResponseUpdate().get_response()


class UpdateUserEmail(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(
            self,
            request
    ):
        email_serializer = EmailFieldSerializer(data=request.data)

        email_serializer.is_valid()
        if email_serializer.errors:
            return ResponseEmailFieldEmptyError().get_response()

        deserializer_data = email_serializer.validated_data

        user_id = request.user.id
        user = User.objects.filter(pk=user_id).first()

        user.email = deserializer_data["email"]
        user.save()

        return ResponseUpdate().get_response()


class UpdateUserPhoneNumber(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(
            self,
            request
    ):
        phone_number_serializer = PhoneNumberFieldSerializer(data=request.data)

        phone_number_serializer.is_valid()
        if phone_number_serializer.errors:
            return ResponsePhoneNumberFieldEmptyError().get_response()

        deserializer_data = phone_number_serializer.validated_data

        user_id = request.user.id
        user = User.objects.filter(pk=user_id).first()

        user.phone_number = deserializer_data["phone_number"]
        user.save()

        return ResponseUpdate().get_response()
