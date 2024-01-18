from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response

from user.models import Profile
from user.serializer import EditProfileInfoSerializer

from util.success_resp_data import UpdateSuccess
from util.error_resp_data import FieldsEmptyError


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
            return Response(
                status=FieldsEmptyError().get_status(),
                data=FieldsEmptyError().get_data()
            )

        user_id = request.user.id
        profile = Profile.objects.filter(user__id=user_id).first()

        serializer_data = serializer.validated_data

        profile.first_name = serializer_data["first_name"]
        profile.second_name = serializer_data["last_name"]

        profile.save()

        return Response(
            status=UpdateSuccess().get_status(),
            data=UpdateSuccess().get_data()
        )
