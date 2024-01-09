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
    EmployerProfile,
    EmployeeProfile,
    EmployeeSpecialization
)


class EditEmployeeProfileSpecializationSerializer(serializers.Serializer):
    id = serializers.ListField(
        child=serializers.IntegerField()
    )
    name = serializers.ListField(
        child=serializers.CharField()
    )


class EditProfileInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            "first_name",
            "second_name",
        ]


class GenerateResetPasswordTOTPSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=150)

    def validate_email(self, value):
        user = User.objects.filter(email=value).first()

        if not user:
            raise serializers.ValidationError(
                "User with given email not found"
            )

        return value


class EmployerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployerProfile
        fields = ["projects_total"]


class EmployeeSpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeSpecialization
        fields = [
            "id",
            "name",
        ]


class EmployeeProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeProfile
        fields = [
            "projects_compleat",
            "specialization",
        ]
        specialization = EmployeeSpecializationSerializer(
            many=True,
        )


class ProfileInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            "id",
            "first_name",
            "second_name",
            "employee_profile",
            "employer_profile",
            "user_avatar",
        ]

    employee_profile = EmployeeProfileSerializer()
    employer_profile = EmployerProfileSerializer()
    user_avatar = serializers.URLField(
        source="user_avatar.user_avatar_url",
        required=False
    )


class RegisterNewUserSerializer(serializers.Serializer):
    email = serializers.EmailField(
        max_length=150,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    phone_number = serializers.CharField(
        style={'base_template': 'textarea.html'},
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(max_length=128)
    is_employer = serializers.BooleanField()
    is_employee = serializers.BooleanField()
    first_name = serializers.CharField(max_length=150)
    second_name = serializers.CharField(max_length=150)


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
                "User with given email not found"
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
            raise serializers.ValidationError("Invalid image extension")

        if value.size > IMAGE_MAX_MEMORY_SIZE:
            raise serializers.ValidationError("Image size to large")


class UpdatePhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "phone_number"
        ]


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "phone_number",
            "date_joined",
            "is_employer",
            "is_employee",
            "is_two_factor_auth",
        ]


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
                "User with given email not found"
            )

        return value


class ValidateTOTPTokenSerializer(serializers.Serializer):
    totp_token = serializers.CharField()
