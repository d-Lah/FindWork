from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from resume.models import Resume
from resume.serializer import ResumeInfoSerializer

from util import success_resp_data
from util.permissions import IsResumeFound


class ResumeInfo(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [
        IsAuthenticated,
        IsResumeFound
    ]

    def get(
            self,
            request,
            resume_id
    ):
        resume = Resume.objects.filter(
            id=resume_id,
            is_delete=False
        ).first()

        serializer = ResumeInfoSerializer(resume)

        serializer_data = serializer.data

        resp_data = success_resp_data.get["data"]
        resp_data["request_data"] = serializer_data

        return Response(
            status=success_resp_data.get["status_code"],
            data=resp_data
        )
