from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from user.models import User
from user.serializer import UserInfoSerializer

from util.success_resp_data import GetSuccess


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

        return Response(
            status=GetSuccess().get_status(),
            data=GetSuccess().get_data(serializer_data)
        )
