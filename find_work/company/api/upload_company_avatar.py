from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from company.models import (
    Company,
    CompanyAvatar
)
from company.serializer import UploadCompanyAvatarSerializer

from util.permissions import (
    IsCompanyOwner,
    IsCompanyFound
)
from util import success_resp_data


class UploadCompanyAvatar(APIView):

    parser_classes = [MultiPartParser]
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
        serializer = UploadCompanyAvatarSerializer(data=request.FILES)

        serializer.is_valid(raise_exception=True)

        serializer_data = serializer.validated_data

        company = Company.objects.filter(
            pk=company_id,
            is_delete=False
        ).first()

        new_company_avatar = CompanyAvatar.objects.create(
            for_company=company,
            company_avatar_url=serializer_data["company_avatar_url"]
        )

        company.user_avatar = new_company_avatar
        company.save()

        return Response(
            status=success_resp_data.upload["status_code"],
            data=success_resp_data.upload["data"]
        )
