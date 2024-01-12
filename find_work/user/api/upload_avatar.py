from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from user.models import (
    Profile,
    UserAvatar,
)
from user.serializer import UploadAvatarSerializer

from util.user_api_resp.upload_avatar_resp import (
    UploadAvatarResp
)


def is_fields_empty(errors):
    if not errors.get("user_avatar_url"):
        return False

    if errors["user_avatar_url"][0] == "No file was submitted.":
        return True

    return False


def is_file_size_to_large(errors):
    if not errors.get("user_avatar_url"):
        return False

    if errors["user_avatar_url"][0] == "Image size to large":
        return True

    return False


def is_invalid_image_extension(errors):
    if not errors.get("user_avatar_url"):
        return False

    if errors["user_avatar_url"][0] == "Invalid image extension":
        return True

    return False


class UploadAvatar(APIView):

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
            return UploadAvatarResp().resp_fields_empty_error()

        if is_invalid_image_extension(serializer.errors):
            return UploadAvatarResp().resp_invalid_file_ext_error()

        if is_file_size_to_large(serializer.errors):
            return UploadAvatarResp().resp_file_size_to_large_error()

        serialized_data = serializer.validated_data

        new_user_avatar = UserAvatar(
            user_avatar_url=serialized_data["user_avatar_url"]
        )

        user_id = request.user.id
        profile = Profile.objects.filter(user__id=user_id).first()

        new_user_avatar.for_profile = profile
        new_user_avatar.user_avatar_url = serialized_data["user_avatar_url"]
        new_user_avatar.save()

        profile.user_avatar = new_user_avatar
        profile.save()

        return UploadAvatarResp().resp_upload()
