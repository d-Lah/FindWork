from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from user.models import User
from user.serializer import UpdateEmailSerializer

from util import success_resp_data


class UpdateEmail(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(
            self,
            request
    ):
        serializer = UpdateEmailSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer_data = serializer.validated_data

        user_id = request.user.id
        user = User.objects.filter(pk=user_id).first()

        user.email = serializer_data["email"]
        user.save()

        return Response(
            status=success_resp_data.update["status_code"],
            data=success_resp_data.update["data"]
        )
