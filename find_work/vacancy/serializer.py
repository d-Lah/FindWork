from django.db import DataError

from rest_framework import serializers
from rest_framework.utils.representation import smart_repr

from vacancy.models import Vacancy

from company.serializer import CompanyInfoSerializer

from resume.serializer import ResumeInfoSerializer

from skill.models import Skill
from skill.serializer import SkillSerializer

from specialization.models import Specialization
from specialization.serializer import SpecializationSerializer

from work_experience.models import WorkExperience
from work_experience.serializer import WorkExperienceSerializer

from type_of_employment.models import TypeOfEmployment
from type_of_employment.serializer import TypeOfEmploymentSerializer

from util.validator import FieldExistsValidator


class CreateVacancySerializer(serializers.Serializer):
    title = serializers.CharField()
    body = serializers.CharField()
    rqd_specialization = serializers.IntegerField(
        validators=[FieldExistsValidator(Specialization.objects.all())]
    )
    rqd_work_experience = serializers.IntegerField(
        validators=[FieldExistsValidator(WorkExperience.objects.all())]
    )
    rqd_skill = serializers.ListField(
        child=serializers.IntegerField(
            validators=[FieldExistsValidator(Skill.objects.all())]
        ),
    )
    rqd_type_of_employment = serializers.ListField(
        child=serializers.IntegerField(
            validators=[FieldExistsValidator(TypeOfEmployment.objects.all())]
        ),
    )


class VacancyInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacancy
        fields = [
            "id",
            "body",
            "title",
            "resumes",
            "company",
            "is_close",
            "rqd_skill",
            "is_delete",
            "date_created",
            "rqd_specialization",
            "rqd_work_experience",
            "rqd_type_of_employment",
        ]

    company = CompanyInfoSerializer()
    rqd_skill = SkillSerializer(many=True)
    resumes = ResumeInfoSerializer(many=True)
    rqd_specialization = SpecializationSerializer()
    rqd_work_experience = WorkExperienceSerializer()
    rqd_type_of_employment = TypeOfEmploymentSerializer(many=True)


class EditVacancyInfoSerializer(serializers.Serializer):
    title = serializers.CharField()
    body = serializers.CharField()
    rqd_specialization = serializers.IntegerField(
        validators=[FieldExistsValidator(Specialization.objects.all())]
    )
    rqd_work_experience = serializers.IntegerField(
        validators=[FieldExistsValidator(WorkExperience.objects.all())]
    )
    rqd_skill = serializers.ListField(
        child=serializers.IntegerField(
            validators=[FieldExistsValidator(Skill.objects.all())]
        ),
    )
    rqd_type_of_employment = serializers.ListField(
        child=serializers.IntegerField(
            validators=[FieldExistsValidator(TypeOfEmployment.objects.all())]
        ),
    )
