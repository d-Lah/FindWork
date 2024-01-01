from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from user.models import User
from user.serializer import UpdatePhoneNumberSerializer

from util.user_api_resp.update_phone_number_resp import UpdatePhoneNumberResp


def is_fields_empty(errors):
    if not errors.get("phone_number"):
        return False

    if "blank" in errors["phone_number"][0]:
        return True

    return False


def is_phone_number_already_exists(errors):
    if not errors.get("phone_number"):
        return False

    if "phone number already exists" in errors["phone_number"][0]:
        return True

    return False


class UpdatePhoneNumber(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(
            self,
            request
    ):
        serializer = UpdatePhoneNumberSerializer(data=request.data)

        serializer.is_valid()

        if is_fields_empty(serializer.errors):
            return UpdatePhoneNumberResp().resp_fields_empty_error()

        if is_phone_number_already_exists(serializer.errors):
            return UpdatePhoneNumberResp(
            ).resp_phone_number_already_exists_error()

        serializer_data = serializer.validated_data

        user_id = request.user.id
        user = User.objects.filter(pk=user_id).first()

        user.phone_number = serializer_data["phone_number"]
        user.save()

        return UpdatePhoneNumberResp().resp_update()
