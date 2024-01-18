from rest_framework import serializers

from resume.models import (
    Skill,
    Specialization,
    WorkExperience,
    TypeOfEmployment
)

from util.error_resp_data import FieldsNotFoundError


class CreateResumeSerializer(serializers.Serializer):
    about = serializers.CharField()
    specialization = serializers.IntegerField()
    work_experience = serializers.IntegerField()
    skill = serializers.ListField(
        child=serializers.IntegerField()
    )
    type_of_employment = serializers.ListField(
        child=serializers.IntegerField()
    )

    def validate_specialization(self, value):
        specialization = Specialization.objects.filter(pk=value).first()

        if not specialization:
            raise serializers.ValidationError("Specialization not found")
        return value

    def validate_skill(self, value):
        for id in value:
            skill = Skill.objects.filter(pk=id).first()

            if not skill:
                raise serializers.ValidationError("Skill not found")
        return value

    def validate_work_experience(self, value):
        work_experience = WorkExperience.objects.filter(pk=value).first()

        if not work_experience:
            raise serializers.ValidationError("Work experience not found")
        return value

    def validate_type_of_employment(self, value):
        for id in value:
            type_of_employment = TypeOfEmployment.objects.filter(
                pk=id
            ).first()

            if not type_of_employment:
                raise serializers.ValidationError(
                    "Type of employment not found"
                )
        return value
