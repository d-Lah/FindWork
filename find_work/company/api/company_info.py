from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from company.models import Company
from company.serializer import CompanyInfoSerializer

from util import success_resp_data
from util.permissions import IsCompanyFound


class CompanyInfo(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [
        IsAuthenticated,
        IsCompanyFound
    ]

    def get(
            self,
            request,
            company_id
    ):
        company = Company.objects.filter(
            id=company_id,
            is_delete=False
        ).first()

        serializer = CompanyInfoSerializer(company)

        serializer_data = serializer.data

        resp_data = success_resp_data.get["data"]
        resp_data["request_data"] = serializer_data

        return Response(
            status=success_resp_data.get["status_code"],
            data=resp_data
        )
