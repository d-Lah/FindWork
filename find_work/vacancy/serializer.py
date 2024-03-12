from rest_framework import serializers

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

from util.error_resp_data import (
    SkillNotFoundError,
    SpecializationNotFoundError,
    WorkExperienceNotFoundError,
    TypeOfEmploymentNotFoundError
)


class CreateVacancySerializer(serializers.Serializer):
    title = serializers.CharField()
    body = serializers.CharField()
    rqd_specialization = serializers.IntegerField()
    rqd_work_experience = serializers.IntegerField()
    rqd_skill = serializers.ListField(
        child=serializers.IntegerField()
    )
    rqd_type_of_employment = serializers.ListField(
        child=serializers.IntegerField()
    )

    def validate_rqd_specialization(self, value):
        specialization = Specialization.objects.filter(pk=value).first()

        if not specialization:
            raise serializers.ValidationError(
                SpecializationNotFoundError().get_data()["specialization"]
            )
        return value

    def validate_rqd_skill(self, value):
        for id in value:
            skill = Skill.objects.filter(pk=id).first()

            if not skill:
                raise serializers.ValidationError(
                    SkillNotFoundError().get_data()["skill"]
                )
        return value

    def validate_rqd_work_experience(self, value):
        work_experience = WorkExperience.objects.filter(pk=value).first()

        if not work_experience:
            raise serializers.ValidationError(
                WorkExperienceNotFoundError().get_data()["work_experience"]
            )
        return value

    def validate_rqd_type_of_employment(self, value):
        for id in value:
            type_of_employment = TypeOfEmployment.objects.filter(
                pk=id
            ).first()

            if not type_of_employment:
                raise serializers.ValidationError(
                    TypeOfEmploymentNotFoundError(
                    ).get_data()["type_of_employment"]
                )
        return value


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
