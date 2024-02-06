from rest_framework import serializers

from user.serializer import UserInfoSerializer

from company.models import Company


class CreateCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = [
            "name",
        ]


class CompanyInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = [
            "id",
            "name",
            "author",
            "company_avatar"
        ]
    author = UserInfoSerializer()
    company_avatar = serializers.URLField(
        source="company_avatar.company_avatar_url",
        required=False
    )


class EditCompanyInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = [
            "name",
        ]
