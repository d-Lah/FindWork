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

from util.validator import FieldExistsValidator


class InsertDataResumeSerializer(serializers.Serializer):
    about = serializers.CharField()
    specialization = serializers.IntegerField(
        validators=[FieldExistsValidator(Specialization.objects.all())]
    )
    work_experience = serializers.IntegerField(
        validators=[FieldExistsValidator(WorkExperience.objects.all())]
    )
    skill = serializers.ListField(
        child=serializers.IntegerField(
            validators=[FieldExistsValidator(Skill.objects.all())]
        ),
    )
    type_of_employment = serializers.ListField(
        child=serializers.IntegerField(
            validators=[FieldExistsValidator(TypeOfEmployment.objects.all())]
        ),
    )

    def create(self, validated_data):
        specialization = Specialization.objects.filter(
            pk=validated_data["specialization"]
        ).first()

        work_experience = WorkExperience.objects.filter(
            pk=validated_data["work_experience"]
        ).first()

        new_resume = Resume.objects.create(
            about=validated_data["about"],
            author=validated_data["author"],
            specialization=specialization,
            work_experience=work_experience,
        )

        skill_list = []

        for id in validated_data["skill"]:
            skill = Skill.objects.filter(pk=id).first()
            skill_list.append(skill)

        type_of_employment_list = []

        for id in validated_data["type_of_employment"]:
            type_of_employment = TypeOfEmployment.objects.filter(
                pk=id
            ).first()
            type_of_employment_list.append(type_of_employment)

        for skill in skill_list:
            new_resume.skill.add(skill)

        for type_of_employment in type_of_employment_list:
            new_resume.type_of_employment.add(type_of_employment)

        return new_resume

    def update(self, instance, validated_data):
        specialization = Specialization.objects.filter(
            pk=validated_data["specialization"]
        ).first()

        work_experience = WorkExperience.objects.filter(
            pk=validated_data["work_experience"]
        ).first()

        skill_list = []

        for id in validated_data["skill"]:
            skill = Skill.objects.filter(pk=id).first()
            skill_list.append(skill)

        type_of_employment_list = []

        for id in validated_data["type_of_employment"]:
            type_of_employment = TypeOfEmployment.objects.filter(
                pk=id
            ).first()
            type_of_employment_list.append(type_of_employment)

        instance.about = validated_data["about"]
        instance.specialization = specialization
        instance.work_experience = work_experience
        instance.skill.all().exclude()
        instance.type_of_employment.all().exclude()

        instance.save()

        for skill in skill_list:
            instance.skill.add(skill)

        for type_of_employment in type_of_employment_list:
            instance.type_of_employment.add(type_of_employment)

        return instance


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
