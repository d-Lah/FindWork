from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from company.models import Company
from company.serializer import CompanyInfoSerializer

from util.success_resp_data import GetSuccess
from util.error_resp_data import CompanyNotFoundError


class CompanyInfo(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(
            self,
            request,
            company_id
    ):
        company = Company.objects.filter(
            id=company_id,
            is_delete=False
        ).first()

        if not company:
            return Response(
                status=CompanyNotFoundError().get_status(),
                data=CompanyNotFoundError().get_data()
            )

        serializer = CompanyInfoSerializer(company)

        serializer_data = serializer.data

        return Response(
            status=GetSuccess().get_status(),
            data=GetSuccess().get_data(serializer_data)
        )
