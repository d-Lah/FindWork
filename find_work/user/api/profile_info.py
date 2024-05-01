from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from user.models import Profile
from user.serializer import ProfileInfoSerializer

from util import success_resp_data
from util.permissions import IsUserFound


class ProfileInfo(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [
        IsAuthenticated,
        IsUserFound
    ]

    def get(
            self,
            request,
            user_id
    ):
        profile = Profile.objects.filter(user__id=user_id).first()

        serializer = ProfileInfoSerializer(profile)

        serializer_data = serializer.data

        resp_data = success_resp_data.get["data"]
        resp_data["request_data"] = serializer_data

        return Response(
            status=success_resp_data.get["status_code"],
            data=resp_data
        )
