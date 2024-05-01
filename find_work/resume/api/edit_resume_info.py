from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from resume.models import Resume

from resume.serializer import InsertDataResumeSerializer

from util.permissions import (
    IsResumeFound,
    IsResumeOwner
)
from util import success_resp_data


class EditResumeInfo(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [
        IsAuthenticated,
        IsResumeFound,
        IsResumeOwner
    ]

    def put(
            self,
            request,
            resume_id
    ):
        resume = Resume.objects.filter(pk=resume_id).first()

        serializer = InsertDataResumeSerializer(resume, data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            status=success_resp_data.update["status_code"],
            data=success_resp_data.update["data"]
        )
