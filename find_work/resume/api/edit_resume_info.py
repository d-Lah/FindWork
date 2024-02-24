from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from resume.models import (
    Skill,
    Resume,
    Specialization,
    WorkExperience,
    TypeOfEmployment
)
from resume.serializer import UpdateResumeInfoSerializer

from util.error_resp_data import (
    FieldsEmptyError,
    FieldsNotFoundError,
    ResumeNotFoundError,
)
from util.error_exceptions import (
    IsFieldsEmpty,
    IsFieldsNotFound
)
from util.permissions import IsEmployee
from util.success_resp_data import UpdateSuccess
from util.error_validation import ErrorValidation


class EditResumeInfo(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [
        IsAuthenticated,
        IsEmployee
    ]

    def put(
            self,
            request,
    ):
        serializer = UpdateResumeInfoSerializer(data=request.data)

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

        user_id = request.user.id
        resume = Resume.objects.filter(
            author__id=user_id,
            is_delete=False
        ).first()

        if not resume:
            return Response(
                status=ResumeNotFoundError().get_status(),
                data=ResumeNotFoundError().get_data()
            )

        serializer_data = serializer.validated_data

        specialization = Specialization.objects.filter(
            pk=serializer_data["specialization"]
        ).first()

        work_experience = WorkExperience.objects.filter(
            pk=serializer_data["work_experience"]
        ).first()

        skill_list = []

        for id in serializer_data["skill"]:
            skill = Skill.objects.filter(pk=id).first()
            skill_list.append(skill)

        type_of_employment_list = []

        for id in serializer_data["type_of_employment"]:
            type_of_employment = TypeOfEmployment.objects.filter(
                pk=id
            ).first()
            type_of_employment_list.append(type_of_employment)

        resume.about = serializer_data["about"]
        resume.specialization = specialization
        resume.work_experience = work_experience
        resume.skill.all().exclude()
        resume.type_of_employment.all().exclude()

        resume.save()

        for skill in skill_list:
            resume.skill.add(skill)

        for type_of_employment in type_of_employment_list:
            resume.type_of_employment.add(type_of_employment)

        return Response(
            status=UpdateSuccess().get_status(),
            data=UpdateSuccess().get_data()
        )
