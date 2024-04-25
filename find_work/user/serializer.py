from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from find_work.settings import (
    ALLOWED_IMAGE_EXT,
    IMAGE_MAX_MEMORY_SIZE
)

from user.models import (
    User,
    Profile,
    UserAvatar,
)

from util import error_resp_data
from util.exceptions import (
    NotFoundException,
    InvalidFileExtException,
    FileSizeTooLargeException,
)


class EditProfileInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            "first_name",
            "last_name",
        ]


class GenerateResetPasswordTOTPSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=150)

    def validate_email(self, value):
        user = User.objects.filter(email=value).first()

        if not user:
            raise NotFoundException(
                error_resp_data.user_with_given_email_not_found
            )

        return value


class ProfileInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            "id",
            "first_name",
            "last_name",
            "user_avatar",
        ]
    user_avatar = serializers.URLField(
        source="user_avatar.user_avatar_url",
        required=False
    )


class RegisterNewUserSerializer(serializers.Serializer):
    email = serializers.EmailField(
        max_length=150,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(max_length=128)
    is_employer = serializers.BooleanField()
    is_employee = serializers.BooleanField()
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)


class ResetPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "email",
            "password"
        ]
    email = serializers.EmailField(max_length=150)

    def validate_email(self, value):
        user = User.objects.filter(email=value).first()

        if not user:
            raise NotFoundException(
                error_resp_data.user_with_given_email_not_found
            )
        return value


class UpdateEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(
        max_length=150,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )


class UpdatePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128)
    new_password = serializers.CharField(max_length=128)


class UploadAvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAvatar
        fields = ["user_avatar_url"]

    user_avatar_url = serializers.FileField(write_only=True)

    def validate_user_avatar_url(self, value):
        image_ext = value.name.split(".")[1]
        if image_ext not in ALLOWED_IMAGE_EXT:
            raise InvalidFileExtException(error_resp_data.invalid_file_ext)

        if value.size > IMAGE_MAX_MEMORY_SIZE:
            raise FileSizeTooLargeException(
                error_resp_data.file_size_too_large
            )


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "resume",
            "company",
            "date_joined",
            "is_employer",
            "is_employee",
            "is_two_factor_auth",
        ]
        resume = serializers.IntegerField(
            source="resume.id",
            required=False
        )
        company = serializers.IntegerField(
            source="company.id",
            required=False
        )


class ValidateResetPasswordTOTPSerializer(serializers.Serializer):
    reset_password_totp = serializers.CharField()
    email = serializers.EmailField(max_length=150)

    def validate_email(self, value):
        user = User.objects.filter(email=value).first()

        if not user:
            raise NotFoundException(
                error_resp_data.user_with_given_email_not_found
            )

        return value


class ValidateTOTPSerializer(serializers.Serializer):
    totp = serializers.CharField()
