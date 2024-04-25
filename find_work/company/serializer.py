from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from find_work.settings import (
    ALLOWED_IMAGE_EXT,
    IMAGE_MAX_MEMORY_SIZE
)

from user.serializer import UserInfoSerializer

from company.models import (
    Company,
    CompanyAvatar
)

from util.exceptions import (
    InvalidFileExtException,
    FileSizeTooLargeException
)
from util import error_resp_data


class CreateCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = [
            "name",
        ]
    name = serializers.CharField(
        validators=[UniqueValidator(queryset=Company.objects.all())]
    )


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
    name = serializers.CharField(
        validators=[UniqueValidator(queryset=Company.objects.all())]
    )


class UploadCompanyAvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyAvatar
        fields = ["company_avatar_url"]

    company_avatar_url = serializers.FileField(write_only=True)

    def validate_company_avatar_url(self, value):
        image_ext = value.name.split(".")[1]
        if image_ext not in ALLOWED_IMAGE_EXT:
            raise InvalidFileExtException(error_resp_data.invalid_file_ext)

        if value.size > IMAGE_MAX_MEMORY_SIZE:
            raise FileSizeTooLargeException(
                error_resp_data.file_size_too_large
            )
