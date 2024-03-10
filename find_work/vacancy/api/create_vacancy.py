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

from util.error_resp_data import (
    FieldsEmptyError,
    FieldsNotFoundError,
)
from util.error_exceptions import (
    IsFieldsEmpty,
    IsFieldsNotFound
)
from util.permissions import (
    IsCompanyOwner
)
from util.success_resp_data import CreateSuccess
from util.error_validation import ErrorValidation


class CreateVacancy(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [
        IsAuthenticated,
        IsCompanyOwner
    ]

    def post(
            self,
            request
    ):
        serializer = CreateVacancySerializer(data=request.data)

        serializer.is_valid()

        error_validation = ErrorValidation(serializer.errors)
        try:
            error_validation.is_fields_empty()
            error_validation.is_fields_not_found()
        except IsFieldsEmpty:
            return Response(
                status=FieldsEmptyError().get_status(),
                data=FieldsEmptyError().get_data()
            )
        except IsFieldsNotFound:
            errors = {}
            for field in serializer.errors:
                error_msg = str(serializer.errors[field][0])
                errors[field] = error_msg

            return Response(
                status=FieldsNotFoundError().get_status(),
                data=errors
            )

        serializer_data = serializer.validated_data

        user_id = request.user.id
        company = Company.objects.filter(author__id=user_id).first()

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
            status=CreateSuccess().get_status(),
            data=CreateSuccess().get_data()
        )
