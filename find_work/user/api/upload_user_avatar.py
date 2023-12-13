from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from user.models import (
    Profile,
    UserAvatar,
)
from user.serializer import UserAvatarSerializer
from user.apps_for_user.user_data_validators import ValidateImageSizeAndExt

from apps.object_exception import (
    InvalidImageExtError,
    ImageSizeToLargeError,
)
from apps.response_error import (
    ResponseInvalidImageExtError,
    ResponseImageSizeTooLargeError,
    ResponseUserAvatarFieldEmptyError,
)
from apps.response_success import ResponseUpload


class UploadUserAvatar(APIView):

    parser_classes = [MultiPartParser]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(
            self,
            request
    ):
        user_avatar_serializer = UserAvatarSerializer(data=request.FILES)

        user_avatar_serializer.is_valid()
        if user_avatar_serializer.errors:
            return ResponseUserAvatarFieldEmptyError().get_response()

        deserialized_data = user_avatar_serializer.validated_data

        image_validators = ValidateImageSizeAndExt(
            deserialized_data["user_avatar_url"]
        )

        try:
            image_validators.is_image_size_too_large()
            image_validators.is_valid_image_ext()

        except ImageSizeToLargeError:
            return ResponseImageSizeTooLargeError().get_response()

        except InvalidImageExtError:
            return ResponseInvalidImageExtError().get_response()

        new_user_avatar = UserAvatar(
            user_avatar_url=deserialized_data.get("user_avatar_url")
        )

        user_id = request.user.id
        profile = Profile.objects.filter(user__id=user_id).first()

        new_user_avatar.for_profile = profile
        new_user_avatar.user_avatar_url = deserialized_data["user_avatar_url"]
        new_user_avatar.save()

        profile.user_avatar = new_user_avatar
        profile.save()

        return ResponseUpload().get_response()
