from rest_framework import serializers

from specialization.models import Specialization


class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = [
            "id",
            "specialization_name"
        ]
