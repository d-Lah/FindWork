from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from resume.serializer import InsertDataResumeSerializer

from util import success_resp_data
from util.permissions import IsEmployee


class CreateResume(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [
        IsAuthenticated,
        IsEmployee
    ]

    def post(
            self,
            request
    ):
        serializer = InsertDataResumeSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        author = request.user

        serializer.save(author=author)

        return Response(
            status=success_resp_data.create["status_code"],
            data=success_resp_data.create["data"],
        )
