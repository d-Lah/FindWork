from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from company.models import Company


class CreateCompanySerializer(serializers.Serializer):
    name = serializers.CharField(
        validators=[UniqueValidator(queryset=Company.objects.all())]
    )
