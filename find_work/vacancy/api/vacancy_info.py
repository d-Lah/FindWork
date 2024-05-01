from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from vacancy.models import Vacancy
from vacancy.serializer import VacancyInfoSerializer

from util import success_resp_data
from util.permissions import IsVacancyFound


class VacancyInfo(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [
        IsAuthenticated,
        IsVacancyFound
    ]

    def get(
            self,
            request,
            vacancy_id
    ):
        resume = Vacancy.objects.filter(
            id=vacancy_id,
            is_delete=False
        ).first()

        serializer = VacancyInfoSerializer(resume)

        serializer_data = serializer.data

        resp_data = success_resp_data.get["data"]
        resp_data["request_data"] = serializer_data

        return Response(
            status=success_resp_data.get["status_code"],
            data=resp_data
        )
