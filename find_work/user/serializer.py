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

from util.error_resp_data import (
    UserNotFoundError,
    InvalidFileExtError,
    FileSizeTooLargeError
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
            raise serializers.ValidationError(
                UserNotFoundError().get_data()["user"]
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
            raise serializers.ValidationError(
                UserNotFoundError().get_data()["user"]
            )
        return value


class UpdateEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "email",
        ]


class UpdatePasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "password"
        ]


class UploadAvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAvatar
        fields = ["user_avatar_url"]

    user_avatar_url = serializers.FileField(write_only=True)

    def validate_user_avatar_url(self, value):
        image_ext = value.name.split(".")[1]
        if image_ext not in ALLOWED_IMAGE_EXT:
            raise serializers.ValidationError(
                InvalidFileExtError().get_data()["file"]
            )

        if value.size > IMAGE_MAX_MEMORY_SIZE:
            raise serializers.ValidationError(
                FileSizeTooLargeError().get_data()["file"]
            )


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "date_joined",
            "is_employer",
            "is_employee",
            "is_two_factor_auth",
            "resume",
        ]
        resume = serializers.IntegerField(
            source="resume.id",
            required=False
        )


class ValidatePasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["password"]


class ValidateResetPasswordTOTPSerializer(serializers.Serializer):
    reset_password_totp = serializers.CharField()
    email = serializers.EmailField(max_length=150)

    def validate_email(self, value):
        user = User.objects.filter(email=value).first()

        if not user:
            raise serializers.ValidationError(
                UserNotFoundError().get_data()["user"]
            )

        return value


class ValidateTOTPTokenSerializer(serializers.Serializer):
    totp_token = serializers.CharField()
