from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from company.models import Company

from vacancy.serializer import InsertDataVacancySerializer

from util.permissions import (
    IsCompanyOwner,
    IsCompanyFound
)
from util import success_resp_data


class CreateVacancy(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [
        IsAuthenticated,
        IsCompanyFound,
        IsCompanyOwner
    ]

    def post(
            self,
            request,
            company_id
    ):
        serializer = InsertDataVacancySerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        company = Company.objects.filter(pk=company_id).first()

        serializer.save(company=company)

        return Response(
            status=success_resp_data.create["status_code"],
            data=success_resp_data.create["data"]
        )
