from rest_framework import serializers

from type_of_employment.models import TypeOfEmployment


class TypeOfEmploymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeOfEmployment
        fields = [
            "id",
            "type_of_employment_name"
        ]
