from rest_framework.views import APIView

from user.models import User
from user.serializer import ResetPasswordSerializer

from util.user_api_resp.reset_password_resp import ResetPasswordResp


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
            return ResetPasswordResp().resp_fields_empty_error()

        if is_invalid_email(serializer.errors):
            return ResetPasswordResp().resp_invalid_email_address_error()

        if is_user_not_found(serializer.errors):
            return ResetPasswordResp().resp_user_not_found_error()

        serializer_data = serializer.validated_data

        user = User.objects.filter(
            email=serializer_data["email"],
        ).first()

        if not user:
            return ResetPasswordResp().resp_user_not_found_error()

        user.set_password(serializer_data["password"])
        user.save()

        return ResetPasswordResp().resp_update()
