from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.authentication import JWTAuthentication

from company.models import Company
from company.serializer import CreateCompanySerializer

from util import success_resp_data
from util.permissions import IsEmployer


class CreateCompany(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [
        IsAuthenticated,
        IsEmployer,
    ]

    def post(
            self,
            request,
    ):
        serializer = CreateCompanySerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        author = request.user

        serializer_data = serializer.validated_data

        Company.objects.create(
            name=serializer_data["name"],
            author=author
        )

        return Response(
            status=success_resp_data.create["status_code"],
            data=success_resp_data.create["data"]
        )
