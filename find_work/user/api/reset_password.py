from rest_framework.views import APIView
from rest_framework.response import Response

from user.models import User
from user.serializer import ResetPasswordSerializer

from util import success_resp_data


class ResetPassword(APIView):
    def put(
            self,
            request
    ):
        serializer = ResetPasswordSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer_data = serializer.validated_data

        user = User.objects.filter(
            email=serializer_data["email"],
        ).first()

        user.set_password(serializer_data["password"])
        user.save()

        return Response(
            status=success_resp_data.update["status_code"],
            data=success_resp_data.update["data"]
        )
