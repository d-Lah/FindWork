from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from user.models import Profile
from user.serializer import ProfileSerializer

from apps.response_success import ResponseUpdate
from apps.response_error import ResponseProfileFieldEmptyError


class EditProfileInfo(APIView):
    """API will edit first name and second name"""

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(
            self,
            request
    ):
        profile_serializer = ProfileSerializer(data=request.data)

        profile_serializer.is_valid()
        if profile_serializer.errors:
            return ResponseProfileFieldEmptyError().get_response()

        user_id = request.user.id
        profile = Profile.objects.filter(user__id=user_id).first()

        deserialized_data = profile_serializer.validated_data

        profile.first_name = deserialized_data["first_name"]
        profile.second_name = deserialized_data["second_name"]

        profile.save()

        return ResponseUpdate().get_response()
