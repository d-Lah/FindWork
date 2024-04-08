from rest_framework import serializers

from user.serializer import UserInfoSerializer

from resume.models import Resume

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
            raise serializers.ValidationError(
                SpecializationNotFoundError().get_data()["specialization"]
            )
        return value

    def validate_skill(self, value):
        for id in value:
            skill = Skill.objects.filter(pk=id).first()

            if not skill:
                raise serializers.ValidationError(
                    SkillNotFoundError().get_data()["skill"]
                )
        return value

    def validate_work_experience(self, value):
        work_experience = WorkExperience.objects.filter(pk=value).first()

        if not work_experience:
            raise serializers.ValidationError(
                WorkExperienceNotFoundError().get_data()["work_experience"]
            )
        return value

    def validate_type_of_employment(self, value):
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


class EditResumeInfoSerializer(serializers.Serializer):
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
            raise serializers.ValidationError(
                SpecializationNotFoundError().get_data()["specialization"]
            )
        return value

    def validate_skill(self, value):
        for id in value:
            skill = Skill.objects.filter(pk=id).first()

            if not skill:
                raise serializers.ValidationError(
                    SkillNotFoundError().get_data()["skill"]
                )
        return value

    def validate_work_experience(self, value):
        work_experience = WorkExperience.objects.filter(pk=value).first()

        if not work_experience:
            raise serializers.ValidationError(
                WorkExperienceNotFoundError().get_data()["work_experience"]
            )
        return value

    def validate_type_of_employment(self, value):
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


class ResumeInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = [
            "id",
            "about",
            "skill",
            "author",
            "is_delete",
            "specialization",
            "work_experience",
            "type_of_employment",
        ]

    author = UserInfoSerializer()
    skill = SkillSerializer(many=True)
    specialization = SpecializationSerializer()
    work_experience = WorkExperienceSerializer()
    type_of_employment = TypeOfEmploymentSerializer(many=True)
