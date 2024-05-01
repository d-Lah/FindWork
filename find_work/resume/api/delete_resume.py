from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from resume.models import Resume

from util import success_resp_data
from util.permissions import (
    IsResumeFound,
    IsResumeOwner
)


class DeleteResume(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [
        IsAuthenticated,
        IsResumeFound,
        IsResumeOwner
    ]

    def delete(
            self,
            request,
            resume_id
    ):
        resume = Resume.objects.filter(pk=resume_id).first()

        resume.is_delete = True
        resume.save()

        return Response(
            status=success_resp_data.delete["status_code"],
            data=success_resp_data.delete["data"]
        )
