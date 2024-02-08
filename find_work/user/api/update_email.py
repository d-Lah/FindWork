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
from util.error_exceptions import (
    IsFieldsEmpty,
    IsFieldsInvalid,
    IsFieldsAlreadyExists,
)
from util.success_resp_data import UpdateSuccess
from util.error_validation import ErrorValidation


class UpdateEmail(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(
            self,
            request
    ):
        serializer = UpdateEmailSerializer(data=request.data)

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

        user_id = request.user.id
        user = User.objects.filter(pk=user_id).first()

        user.email = serializer_data["email"]
        user.save()

        return Response(
            status=UpdateSuccess().get_status(),
            data=UpdateSuccess().get_data()
        )
