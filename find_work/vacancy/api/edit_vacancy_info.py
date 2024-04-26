from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from vacancy.models import Vacancy

from skill.models import Skill

from specialization.models import Specialization

from work_experience.models import WorkExperience

from type_of_employment.models import TypeOfEmployment

from vacancy.serializer import EditVacancyInfoSerializer

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
        serializer = EditVacancyInfoSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer_data = serializer.validated_data

        rqd_specialization = Specialization.objects.filter(
            pk=serializer_data["rqd_specialization"]
        ).first()

        rqd_work_experience = WorkExperience.objects.filter(
            pk=serializer_data["rqd_work_experience"]
        ).first()

        rqd_skill_list = []

        for id in serializer_data["rqd_skill"]:
            rqd_skill = Skill.objects.filter(pk=id).first()
            rqd_skill_list.append(rqd_skill)

        rqd_type_of_employment_list = []

        for id in serializer_data["rqd_type_of_employment"]:
            rqd_type_of_employment = TypeOfEmployment.objects.filter(
                pk=id
            ).first()
            rqd_type_of_employment_list.append(rqd_type_of_employment)

        vacancy = Vacancy.objects.filter(
            pk=vacancy_id,
            is_delete=False
        ).first()

        vacancy.title = serializer_data["title"]
        vacancy.body = serializer_data["body"]
        vacancy.rqd_specialization = rqd_specialization
        vacancy.rqd_work_experience = rqd_work_experience
        vacancy.rqd_skill.all().exclude()
        vacancy.rqd_type_of_employment.all().exclude()

        vacancy.save()

        for rqd_skill in rqd_skill_list:
            vacancy.rqd_skill.add(rqd_skill)

        for rqd_type_of_employment in rqd_type_of_employment_list:
            vacancy.rqd_type_of_employment.add(rqd_type_of_employment)

        return Response(
            status=success_resp_data.update["status_code"],
            data=success_resp_data.update["data"]
        )
