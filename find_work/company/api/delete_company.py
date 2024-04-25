from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from company.models import Company

from util import success_resp_data
from util.permissions import (
    IsCompanyFound,
    IsCompanyOwner,
)


class DeleteCompany(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [
        IsAuthenticated,
        IsCompanyFound,
        IsCompanyOwner
    ]

    def delete(
            self,
            request,
            company_id
    ):

        company = Company.objects.filter(pk=company_id).first()

        company.is_delete = True
        company.save()

        return Response(
            status=success_resp_data.delete["status_code"],
            data=success_resp_data.delete["data"]
        )
