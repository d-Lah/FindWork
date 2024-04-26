from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from user.models import User

from vacancy.models import Vacancy

from company.models import Company

from skill.models import Skill

from specialization.models import Specialization

from work_experience.models import WorkExperience

from type_of_employment.models import TypeOfEmployment


from vacancy.serializer import CreateVacancySerializer

from util.permissions import (
    IsCompanyOwner,
    IsCompanyFound
)
from util import success_resp_data


class CreateVacancy(APIView):
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
        serializer = CreateVacancySerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer_data = serializer.validated_data

        company = Company.objects.filter(
            pk=company_id,
            is_delete=False
        ).first()

        rqd_specialization = Specialization.objects.filter(
            pk=serializer_data["rqd_specialization"]
        ).first()

        rqd_work_experience = WorkExperience.objects.filter(
            pk=serializer_data["rqd_work_experience"]
        ).first()

        new_vacancy = Vacancy.objects.create(
            company=company,
            title=serializer_data["title"],
            body=serializer_data["body"],
            rqd_specialization=rqd_specialization,
            rqd_work_experience=rqd_work_experience
        )

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

        for rqd_skill in rqd_skill_list:
            new_vacancy.rqd_skill.add(rqd_skill)

        for rqd_type_of_employment in rqd_type_of_employment_list:
            new_vacancy.rqd_type_of_employment.add(
                rqd_type_of_employment
            )

        return Response(
            status=success_resp_data.create["status_code"],
            data=success_resp_data.create["data"]
        )
