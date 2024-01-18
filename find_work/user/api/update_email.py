from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from user.models import User
from user.serializer import UpdateEmailSerializer

from util.error_resp_data import (
    FieldsEmptyError,
    InvalidEmailAdressError,
    EmailAlreadyExistsError,
)
from util.success_resp_data import UpdateSuccess


def is_fields_empty(errors):
    if not errors.get("email"):
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


def is_email_already_exists(errors):
    if not errors.get("email"):
        return False

    if "email already exists" in errors["email"][0]:
        return True

    return False


class UpdateEmail(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(
            self,
            request
    ):
        serializer = UpdateEmailSerializer(data=request.data)

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

        if is_email_already_exists(serializer.errors):
            return Response(
                status=EmailAlreadyExistsError().get_status(),
                data=EmailAlreadyExistsError().get_data()
            )

        serializer_data = serializer.validated_data

        user_id = request.user.id
        user = User.objects.filter(pk=user_id).first()

        user.email = serializer_data["email"]
        user.save()

        return Response(
            status=UpdateSuccess().get_status(),
            data=UpdateSuccess().get_data()
        )
