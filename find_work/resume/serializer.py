from rest_framework import serializers

from user.serializer import UserInfoSerializer

from resume.models import (
    Skill,
    Resume,
    Specialization,
    WorkExperience,
    TypeOfEmployment
)
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


class UpdateResumeInfoSerializer(serializers.Serializer):
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


class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = [
            "id",
            "specialization_name"
        ]


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = [
            "id",
            "skill_name"
        ]


class WorkExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkExperience
        fields = [
            "id",
            "work_experience_name"
        ]


class TypeOfEmploymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeOfEmployment
        fields = [
            "id",
            "type_of_employment_name"
        ]


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
