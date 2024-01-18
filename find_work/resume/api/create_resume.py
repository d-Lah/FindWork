from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from user.models import User

from resume.models import (
    Skill,
    Resume,
    Specialization,
    WorkExperience,
    TypeOfEmployment
)
from resume.serializer import CreateResumeSerializer

from util.error_resp_data import (
    FieldsEmptyError,
    FieldsNotFoundError
)
from util.success_resp_data import (
    CreateSuccess
)


def is_fields_empty(errors):
    if not errors:
        return False

    for field in errors:
        if "blank" in errors[field][0]:
            return True
    return False


def is_fields_not_found(errors):
    if not errors:
        return False

    for field in errors:
        if "not found" in errors[field][0]:
            return True
    return False


class CreateResume(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(
            self,
            request
    ):
        serializer = CreateResumeSerializer(data=request.data)

        serializer.is_valid()

        if is_fields_empty(serializer.errors):
            return Response(
                status=FieldsEmptyError().get_status(),
                data=FieldsEmptyError().get_data()
            )

        if is_fields_not_found(serializer.errors):
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

        author = User.objects.filter(pk=user_id).first()

        specialization = Specialization.objects.filter(
            pk=serializer_data["specialization"]
        ).first()

        work_experience = WorkExperience.objects.filter(
            pk=serializer_data["work_experience"]
        ).first()

        new_resume = Resume.objects.create(
            about=serializer_data["about"],
            author=author,
            specialization=specialization,
            work_experience=work_experience,
        )

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

        for skill in skill_list:
            new_resume.skill.add(skill)

        for type_of_employment in type_of_employment_list:
            new_resume.type_of_employment.add(type_of_employment)

        return Response(
            status=CreateSuccess().get_status(),
            data=CreateSuccess().get_data()
        )
