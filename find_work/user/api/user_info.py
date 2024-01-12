from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from user.models import User
from user.serializer import UserInfoSerializer

from util.user_api_resp.user_info_resp import (
    UserInfoResp
)


class UserInfo(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(
            self,
            request
    ):
        user_id = request.user.id
        user = User.objects.filter(pk=user_id).first()

        serializer = UserInfoSerializer(user)

        serializer_data = serializer.data

        return UserInfoResp().resp_get(serializer_data)
