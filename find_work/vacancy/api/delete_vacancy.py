from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from vacancy.models import Vacancy

from util.success_resp_data import DeleteSuccess
from util.permissions import (
    IsVacancyFound,
    IsCompanyOwner,
    IsVacancyCreator,
)


class DeleteVacancy(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [
        IsAuthenticated,
        IsVacancyFound,
        IsCompanyOwner,
        IsVacancyCreator,
    ]

    def delete(
            self,
            request,
            vacancy_id
    ):
        resume = Vacancy.objects.filter(pk=vacancy_id).first()

        resume.is_delete = True
        resume.save()

        return Response(
            status=DeleteSuccess().get_status(),
            data=DeleteSuccess().get_data()
        )
