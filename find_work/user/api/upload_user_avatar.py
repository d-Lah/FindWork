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
from util.error_exceptions import (
    IsFileFieldsEmpty,
    IsFileFieldsInvalid,
    IsFileFieldsSizeTooLarge,
)
from util.success_resp_data import UploadSuccess
from util.error_validation import ErrorValidation


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

        error_validation = ErrorValidation(serializer.errors)
        try:
            error_validation.is_file_fields_empty()
            error_validation.is_file_fields_invalid()
            error_validation.is_file_fields_size_too_large()
        except IsFileFieldsEmpty:
            return Response(
                status=FieldsEmptyError().get_status(),
                data=FieldsEmptyError().get_data()
            )
        except IsFileFieldsInvalid:
            return Response(
                status=InvalidFileExtError().get_status(),
                data=InvalidFileExtError().get_data()
            )
        except IsFileFieldsSizeTooLarge:
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
