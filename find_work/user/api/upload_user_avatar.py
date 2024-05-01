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

from util import success_resp_data


class UploadUserAvatar(APIView):

    parser_classes = [MultiPartParser]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(
            self,
            request
    ):
        serializer = UploadAvatarSerializer(data=request.FILES)

        serializer.is_valid(raise_exception=True)

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
            status=success_resp_data.upload["status_code"],
            data=success_resp_data.upload["data"],
        )
