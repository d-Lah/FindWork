from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from user.models import Profile
from user.serializer import EditProfileInfoSerializer

from util.user_api_resp.edit_profile_info_resp import EditProfileInfoResp


class EditProfileInfo(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(
            self,
            request
    ):
        serializer = EditProfileInfoSerializer(data=request.data)

        serializer.is_valid()
        if serializer.errors:
            return EditProfileInfoResp().resp_fields_empty_error()

        user_id = request.user.id
        profile = Profile.objects.filter(user__id=user_id).first()

        serializer_data = serializer.validated_data

        profile.first_name = serializer_data["first_name"]
        profile.second_name = serializer_data["last_name"]

        profile.save()

        return EditProfileInfoResp().resp_update()
