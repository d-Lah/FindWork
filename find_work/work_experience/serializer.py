from rest_framework import serializers

from work_experience.models import WorkExperience


class WorkExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkExperience
        fields = [
            "id",
            "work_experience_name"
        ]
