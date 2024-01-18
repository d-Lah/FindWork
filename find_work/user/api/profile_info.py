from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from user.models import Profile
from user.serializer import ProfileInfoSerializer

from util.success_resp_data import GetSuccess


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

        return Response(
            status=GetSuccess().get_status(),
            data=GetSuccess().get_data(serializer_data)
        )
