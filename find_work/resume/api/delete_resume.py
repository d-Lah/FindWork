from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from find_work.permissions import IsEmployee

from resume.models import Resume

from util.success_resp_data import DeleteSuccess
from util.error_resp_data import ResumeNotFoundError


class DeleteResume(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [
        IsAuthenticated,
        IsEmployee
    ]

    def delete(
            self,
            request,
    ):

        user_id = request.user.id
        resume = Resume.objects.filter(
            author__id=user_id,
            is_delete=False
        ).first()

        if not resume:
            return Response(
                status=ResumeNotFoundError().get_status(),
                data=ResumeNotFoundError().get_data()
            )

        resume.is_delete = True
        resume.save()

        return Response(
            status=DeleteSuccess().get_status(),
            data=DeleteSuccess().get_data()
        )
