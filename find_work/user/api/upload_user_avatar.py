from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from user.models import (
    Profile,
    UserAvatar,
)
from user.serializer import UploadAvatarSerializer

from util.error_resp_data import (
    FieldsEmptyError,
    InvalidFileExtError,
    FileSizeTooLargeError,
)
from util.success_resp_data import UploadSuccess


def is_fields_empty(errors):
    if not errors.get("user_avatar_url"):
        return False

    if errors["user_avatar_url"][0] == "No file was submitted.":
        return True

    return False


def is_file_size_to_large(errors):
    if not errors.get("user_avatar_url"):
        return False

    error = FileSizeTooLargeError().get_data()["file"]
    if errors["user_avatar_url"][0] == error:
        return True

    return False


def is_invalid_image_extension(errors):
    if not errors.get("user_avatar_url"):
        return False

    error = InvalidFileExtError().get_data()["file"]
    if errors["user_avatar_url"][0] == error:
        return True

    return False


class UploadUserAvatar(APIView):

    parser_classes = [MultiPartParser]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(
            self,
            request
    ):
        serializer = UploadAvatarSerializer(data=request.FILES)

        serializer.is_valid()

        if is_fields_empty(serializer.errors):
            return Response(
                status=FieldsEmptyError().get_status(),
                data=FieldsEmptyError().get_data()
            )

        if is_invalid_image_extension(serializer.errors):
            return Response(
                status=InvalidFileExtError().get_status(),
                data=InvalidFileExtError().get_data()
            )

        if is_file_size_to_large(serializer.errors):
            return Response(
                status=FileSizeTooLargeError().get_status(),
                data=FileSizeTooLargeError().get_data()
            )

        serializer_data = serializer.validated_data

        user_id = request.user.id
        profile = Profile.objects.filter(user__id=user_id).first()

        new_user_avatar = UserAvatar.objects.create(
            for_profile=profile,
            user_avatar_url=serializer_data["user_avatar_url"]
        )

        profile.user_avatar = new_user_avatar
        profile.save()

        return Response(
            status=UploadSuccess().get_status(),
            data=UploadSuccess().get_data()
        )
