from rest_framework import serializers

from find_work.settings import (
    ALLOWED_IMAGE_EXT,
    IMAGE_MAX_MEMORY_SIZE
)

from user.serializer import UserInfoSerializer

from company.models import (
    Company,
    CompanyAvatar
)

from util.error_resp_data import (
    InvalidFileExtError,
    FileSizeTooLargeError
)


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


class UploadCompanyAvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyAvatar
        fields = ["company_avatar_url"]

    company_avatar_url = serializers.FileField(write_only=True)

    def validate_company_avatar_url(self, value):
        image_ext = value.name.split(".")[1]
        if image_ext not in ALLOWED_IMAGE_EXT:
            raise serializers.ValidationError(
                InvalidFileExtError().get_data()["file"]
            )

        if value.size > IMAGE_MAX_MEMORY_SIZE:
            raise serializers.ValidationError(
                FileSizeTooLargeError().get_data()["file"]
            )
