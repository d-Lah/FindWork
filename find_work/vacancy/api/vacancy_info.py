from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from vacancy.models import Vacancy
from vacancy.serializer import VacancyInfoSerializer

from util.success_resp_data import GetSuccess
from util.error_resp_data import VacancyNotFound


class VacancyInfo(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(
            self,
            request,
            vacancy_id
    ):
        resume = Vacancy.objects.filter(
            id=vacancy_id,
            is_delete=False
        ).first()

        if not resume:
            return Response(
                status=VacancyNotFound().get_status(),
                data=VacancyNotFound().get_data()
            )

        serializer = VacancyInfoSerializer(resume)

        serializer_data = serializer.data

        return Response(
            status=GetSuccess().get_status(),
            data=GetSuccess().get_data(serializer_data)
        )
