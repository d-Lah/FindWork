from rest_framework.views import APIView
from rest_framework.response import Response

from user.models import User
from user.serializer import ResetPasswordSerializer

from util.error_resp_data import (
    FieldsEmptyError,
    UserNotFoundError,
    InvalidEmailAdressError,
)
from util.success_resp_data import UpdateSuccess


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


def is_user_not_found(errors):
    if not errors.get("email"):
        return False

    if errors["email"][0] == "User with given email not found":
        return True

    return False


class ResetPassword(APIView):
    def put(
            self,
            request
    ):
        serializer = ResetPasswordSerializer(data=request.data)

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

        user = User.objects.filter(
            email=serializer_data["email"],
        ).first()

        user.set_password(serializer_data["password"])
        user.save()

        return Response(
            status=UpdateSuccess().get_status(),
            data=UpdateSuccess().get_data()
        )
