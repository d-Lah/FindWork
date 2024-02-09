from rest_framework.views import APIView
from rest_framework.response import Response

from user.models import User
from user.serializer import ResetPasswordSerializer

from util.error_resp_data import (
    FieldsEmptyError,
    UserNotFoundError,
    InvalidEmailAdressError,
)
from util.error_exceptions import (
    IsFieldsEmpty,
    IsFieldsInvalid,
    IsFieldsNotFound,
)
from util.success_resp_data import UpdateSuccess
from util.error_validation import ErrorValidation


class ResetPassword(APIView):
    def put(
            self,
            request
    ):
        serializer = ResetPasswordSerializer(data=request.data)

        serializer.is_valid()

        error_validation = ErrorValidation(serializer.errors)
        try:
            error_validation.is_fields_empty()
            error_validation.is_fields_invalid()
            error_validation.is_fields_not_found()
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
        except IsFieldsNotFound:
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
