from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from user.models import Profile
from user.serializer import ProfileInfoSerializer

from util.user_api_resp.profile_info_resp import (
    ProfileInfoResp
)


class ProfileInfo(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(
            self,
            request
    ):
        user_id = request.user.id
        profile = Profile.objects.filter(user__id=user_id).first()

        serializer = ProfileInfoSerializer(profile)

        serializer_data = serializer.data

        return ProfileInfoResp().resp_get(serializer_data)
