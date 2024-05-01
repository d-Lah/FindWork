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

from util.validator import FieldExistsValidator


class InsertDataVacancySerializer(serializers.Serializer):
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

    def create(self, validated_data):
        rqd_specialization = Specialization.objects.filter(
            pk=validated_data["rqd_specialization"]
        ).first()

        rqd_work_experience = WorkExperience.objects.filter(
            pk=validated_data["rqd_work_experience"]
        ).first()

        new_vacancy = Vacancy.objects.create(
            company=validated_data["company"],
            title=validated_data["title"],
            body=validated_data["body"],
            rqd_specialization=rqd_specialization,
            rqd_work_experience=rqd_work_experience
        )

        rqd_skill_list = []

        for id in validated_data["rqd_skill"]:
            rqd_skill = Skill.objects.filter(pk=id).first()
            rqd_skill_list.append(rqd_skill)

        rqd_type_of_employment_list = []

        for id in validated_data["rqd_type_of_employment"]:
            rqd_type_of_employment = TypeOfEmployment.objects.filter(
                pk=id
            ).first()
            rqd_type_of_employment_list.append(rqd_type_of_employment)

        for rqd_skill in rqd_skill_list:
            new_vacancy.rqd_skill.add(rqd_skill)

        for rqd_type_of_employment in rqd_type_of_employment_list:
            new_vacancy.rqd_type_of_employment.add(
                rqd_type_of_employment
            )

        return new_vacancy

    def update(self, instance, validated_data):
        rqd_specialization = Specialization.objects.filter(
            pk=validated_data["rqd_specialization"]
        ).first()

        rqd_work_experience = WorkExperience.objects.filter(
            pk=validated_data["rqd_work_experience"]
        ).first()

        rqd_skill_list = []

        for id in validated_data["rqd_skill"]:
            rqd_skill = Skill.objects.filter(pk=id).first()
            rqd_skill_list.append(rqd_skill)

        rqd_type_of_employment_list = []

        for id in validated_data["rqd_type_of_employment"]:
            rqd_type_of_employment = TypeOfEmployment.objects.filter(
                pk=id
            ).first()
            rqd_type_of_employment_list.append(rqd_type_of_employment)

        instance.title = validated_data["title"]
        instance.body = validated_data["body"]
        instance.rqd_specialization = rqd_specialization
        instance.rqd_work_experience = rqd_work_experience
        instance.rqd_skill.all().exclude()
        instance.rqd_type_of_employment.all().exclude()

        instance.save()

        for rqd_skill in rqd_skill_list:
            instance.rqd_skill.add(rqd_skill)

        for rqd_type_of_employment in rqd_type_of_employment_list:
            instance.rqd_type_of_employment.add(rqd_type_of_employment)

        return instance


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
