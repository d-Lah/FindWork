from rest_framework.views import APIView

from user.models import (
    User,
)
from user.serializer import (
    EmailFieldSerializer,
    PasswordFieldSerializer,
)

from apps.object_exception import (
    EmailFieldEmptyError,
    PasswordFieldEmptyError,
)
from apps.response_error import (
    ResponseUserNotFoundError,
    ResponseEmailFieldEmptyError,
    ResponsePasswordFieldEmptyError,
)
from apps.response_success import ResponseUpdate
from apps.fields_validators import ValidateFieldsOnEmpty


class ResetUserPassword(APIView):
    def put(
            self,
            request
    ):
        email_serializer = EmailFieldSerializer(data=request.data)
        password_serializer = PasswordFieldSerializer(data=request.data)

        email_serializer.is_valid()
        password_serializer.is_valid()

        validate_field = {
            "email": email_serializer.errors,
            "password": password_serializer.errors
        }

        data_validators = ValidateFieldsOnEmpty(
            validate_field
        )

        try:
            data_validators.is_email_field_empty()
            data_validators.is_password_field_empty()

        except EmailFieldEmptyError:
            return ResponseEmailFieldEmptyError().get_response()

        except PasswordFieldEmptyError:
            return ResponsePasswordFieldEmptyError().get_response()

        email_deserilized_data = email_serializer.validated_data

        user = User.objects.filter(
            email=email_deserilized_data["email"],
        ).first()

        if not user:
            return ResponseUserNotFoundError().get_response()

        password_deserialized_data = password_serializer.validated_data

        user.on_reset_password = False
        user.set_password(password_deserialized_data["password"])
        user.save()

        return ResponseUpdate().get_response()
