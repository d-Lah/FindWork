from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from resume.models import Resume
from resume.serializer import ResumeInfoSerializer

from util.success_resp_data import GetSuccess
from util.error_resp_data import ResumeNotFoundError


class ResumeInfo(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(
            self,
            request,
            resume_id
    ):
        resume = Resume.objects.filter(
            id=resume_id,
            is_delete=False
        ).first()

        if not resume:
            return Response(
                status=ResumeNotFoundError().get_status(),
                data=ResumeNotFoundError().get_data()
            )

        serializer = ResumeInfoSerializer(resume)

        serializer_data = serializer.data

        return Response(
            status=GetSuccess().get_status(),
            data=GetSuccess().get_data(serializer_data)
        )
