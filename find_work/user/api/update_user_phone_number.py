from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from user.models import User
from user.serializer import PhoneNumberFieldSerializer

from apps.response_error import (
    ResponsePhoneNumberFieldEmptyError,
    ResponsePhoneNumberAlreadyExistsError,
)
from apps.response_success import ResponseUpdate
from user.apps_for_user.user_data_validators import (
    ValidateEmailAndPhoneNumberOnExists
)
from apps.object_exception import PhoneNuberAlreadyExistsError


class UpdateUserPhoneNumber(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(
            self,
            request
    ):
        phone_number_serializer = PhoneNumberFieldSerializer(data=request.data)

        phone_number_serializer.is_valid()

        deserializer_data = phone_number_serializer.validated_data

        user_data_validators = ValidateEmailAndPhoneNumberOnExists(
            phone_number=deserializer_data.get("phone_number"),
            email=None
        )

        try:
            user_data_validators.is_phone_number_exists()

        except PhoneNuberAlreadyExistsError:
            return ResponsePhoneNumberAlreadyExistsError().get_response()

        if phone_number_serializer.errors:
            return ResponsePhoneNumberFieldEmptyError().get_response()

        user_id = request.user.id
        user = User.objects.filter(pk=user_id).first()

        user.phone_number = deserializer_data["phone_number"]
        user.save()

        return ResponseUpdate().get_response()
