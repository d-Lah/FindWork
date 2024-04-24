from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from user.models import User

from resume.models import Resume

from skill.models import Skill

from specialization.models import Specialization

from work_experience.models import WorkExperience

from type_of_employment.models import TypeOfEmployment

from resume.serializer import CreateResumeSerializer

from util import success_resp_data
from util.permissions import IsEmployee


class CreateResume(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [
        IsAuthenticated,
        IsEmployee
    ]

    def post(
            self,
            request
    ):
        serializer = CreateResumeSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

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
            status=success_resp_data.create["status_code"],
            data=success_resp_data.create["data"],
        )
