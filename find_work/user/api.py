from .models import (
    User,
    Profile,
    EmployerProfile,
    EmployeeProfile,
)
from .serializer import (
    UserSerializer,
    ProfileSerializer,
    UserAvatarSerializer,
    EmployerProfileSerializer,
    EmployeeProfileSerializer,
)
from uuid import (
    uuid4,
)
from find_work.settings import (
    EMAIL_HOST_USER,
    ALLOWED_FILE_EXT,
    FILE_UPLOAD_MAX_MEMORY_SIZE,
)
from django.core.mail import (
    send_mail,
)
from rest_framework.views import (
    APIView,
)
from django.contrib.auth.hashers import (
    make_password,
    check_password,
)
from rest_framework.response import (
    Response,
)
from rest_framework.parsers import (
    MultiPartParser,
)
from rest_framework.permissions import (
    IsAuthenticated,
)
from rest_framework_simplejwt.authentication import (
    JWTAuthentication,
)


class Register(APIView):
    def post(
            self,
            request,
    ):
        user_serializer = UserSerializer(data=request.data)
        user_serializer.is_valid()
        email_to_check = user_serializer.data.get("email")
        email_exists = User.objects.filter(email=email_to_check).exists()

        if email_exists:
            return Response(
                {"error": "EmailAlreadyExists"},
                status=409,
            )

        phone_number_to_check = user_serializer.data.get("phone_number")
        phone_number_exists = User.objects.filter(
            phone_number=phone_number_to_check
        ).exists()

        if phone_number_exists:
            return Response(
                {"error": "PhoneNumberAlreadyExistsError"},
                status=409,
            )

        if user_serializer.errors:
            return Response(
                {"error": "UserFieldEmptyError"},
                status=400,
            )

        data_user = user_serializer.validated_data

        profile_serializer = ProfileSerializer(data=request.data)
        profile_serializer.is_valid()

        if profile_serializer.errors:
            return Response(
                {"error": "ProfileFieldEmptyError"},
                status=400,
            )

        data_profile = profile_serializer.validated_data

        if data_user.get("is_employer"):
            new_employer_profile = EmployerProfile()
            new_employer_profile.save()
        else:
            new_employer_profile = None

        if data_user.get("is_employee"):
            new_employee_profile = EmployeeProfile()
            new_employee_profile.save()
        else:
            new_employee_profile = None

        new_profile = Profile(
            first_name=data_profile.get("first_name"),
            second_name=data_profile.get("second_name"),
            employer_profile=new_employer_profile,
            employee_profile=new_employee_profile,
        )
        new_profile.save()

        new_user = User(
            email=data_user.get("email"),
            phone_number=data_user.get("phone_number"),
            user_activation_uuid=uuid4(),
            profile=new_profile,
            is_employer=data_user.get("is_employer"),
            is_employee=data_user.get("is_employee"),
            password=make_password(data_user.get("password")),
        )

        new_user.save()
        new_user_activation_uuid = new_user.user_activation_uuid
        activate_user_url = "http://localhost:8000/user/activate-user/"
        msg_url = f"{activate_user_url}{new_user_activation_uuid}"
        send_mail(
            subject=f"Hello {new_profile.first_name}",
            message=f"Account activation link {msg_url}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[f"{new_user.email}"],
            fail_silently=False,
        )

        return Response(
            {"status": "Create"},
            status=201,
        )


class ActivateUser(APIView):
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
            return Response(
                {"error": "UserAlreadyActiveError"},
                status=409,
            )
        user.is_active = True
        user.save()
        return Response(
            {"status": "Update"},
            status=200,
        )
