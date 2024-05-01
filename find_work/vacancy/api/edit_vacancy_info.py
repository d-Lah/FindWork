from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from vacancy.models import Vacancy

from vacancy.serializer import InsertDataVacancySerializer

from util.permissions import (
    IsCompanyOwner,
    IsVacancyFound,
    IsVacancyCreator,
)
from util import success_resp_data


class EditVacancyInfo(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [
        IsAuthenticated,
        IsVacancyFound,
        IsCompanyOwner,
        IsVacancyCreator,
    ]

    def put(
            self,
            request,
            vacancy_id
    ):
        vacancy = Vacancy.objects.filter(pk=vacancy_id).first()

        serializer = InsertDataVacancySerializer(vacancy, data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(
            status=success_resp_data.update["status_code"],
            data=success_resp_data.update["data"]
        )
