from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from user.models import User
from user.serializer import EmailFieldSerializer

from apps.response_success import ResponseUpdate
from apps.object_exception import EmailAlreadyExistsError
from apps.response_error import (
    ResponseEmailFieldEmptyError,
    ResponseEmailAlreadyExistsError,
)
from user.apps_for_user.user_data_validators import (
    ValidateEmailAndPhoneNumberOnExists,
)


class UpdateUserEmail(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(
            self,
            request
    ):
        email_serializer = EmailFieldSerializer(data=request.data)

        email_serializer.is_valid()

        deserializer_data = email_serializer.validated_data

        user_data_validators = ValidateEmailAndPhoneNumberOnExists(
            email=deserializer_data.get("email"),
            phone_number=None
        )

        try:
            user_data_validators.is_email_exists()

        except EmailAlreadyExistsError:
            return ResponseEmailAlreadyExistsError().get_response()

        if email_serializer.errors:
            return ResponseEmailFieldEmptyError().get_response()

        user_id = request.user.id
        user = User.objects.filter(pk=user_id).first()

        user.email = deserializer_data["email"]
        user.save()

        return ResponseUpdate().get_response()
