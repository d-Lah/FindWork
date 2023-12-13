from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from user.models import User
from user.serializer import (
    UserSerializer,
    ProfileSerializer,
)

from apps.response_success import ResponseGet


class UserInfo(APIView):
    """API should response data with some user data to show them"""

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(
            self,
            request
    ):
        user_id = request.user.id
        user = User.objects.filter(pk=user_id).first()

        user_serializer = UserSerializer(user)
        profile_serializer = ProfileSerializer(user.profile)

        serialized_user_data = user_serializer.data
        serialized_profile_data = profile_serializer.data

        response_data = ResponseGet()
        response_data.add_data_for_response_data(
            "user_data",
            serialized_user_data
        )
        response_data.add_data_for_response_data(
            "profile_data",
            serialized_profile_data
        )
        return response_data.get_response()
