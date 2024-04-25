from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from company.models import Company
from company.serializer import EditCompanyInfoSerializer

from util.permissions import (
    IsCompanyOwner,
    IsCompanyFound
)
from util import success_resp_data


class EditCompanyInfo(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [
        IsAuthenticated,
        IsCompanyFound,
        IsCompanyOwner
    ]

    def put(
            self,
            request,
            company_id
    ):
        serializer = EditCompanyInfoSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        company = Company.objects.filter(
            pk=company_id,
            is_delete=False
        ).first()

        serializer_data = serializer.validated_data

        company.name = serializer_data["name"]
        company.save()

        return Response(
            status=success_resp_data.update["status_code"],
            data=success_resp_data.update["data"]
        )
