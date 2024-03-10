from rest_framework import serializers

from skill.models import Skill

from specialization.models import Specialization

from work_experience.models import WorkExperience

from type_of_employment.models import TypeOfEmployment

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
