from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from company.models import Company

from util.permissions import IsEmployer
from util.success_resp_data import DeleteSuccess
from util.error_resp_data import CompanyNotFoundError


class DeleteCompany(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [
        IsAuthenticated,
        IsEmployer
    ]

    def delete(
            self,
            request,
    ):

        user_id = request.user.id
        resume = Company.objects.filter(
            author__id=user_id,
            is_delete=False
        ).first()

        if not resume:
            return Response(
                status=CompanyNotFoundError().get_status(),
                data=CompanyNotFoundError().get_data()
            )

        resume.is_delete = True
        resume.save()

        return Response(
            status=DeleteSuccess().get_status(),
            data=DeleteSuccess().get_data()
        )
