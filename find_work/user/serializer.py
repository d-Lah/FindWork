from rest_framework import serializers
from rest_framework.response import Response

from .models import (
    User,
    Profile,
    UserAvatar,
    EmployerProfile,
    EmployeeProfile,
)


class EmployerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployerProfile
        fields = ["projects_total"]
    projects_total = serializers.IntegerField(required=False)


class EmployeeProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeProfile
        fields = ["projects_compleat"]
    projects_compleat = serializers.IntegerField(required=False)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            "first_name",
            "second_name",
            "employee_profile",
            "user_avatar",
        ]
    first_name = serializers.CharField()
    second_name = serializers.CharField()
    employee_profile = EmployeeProfileSerializer(required=False)
    user_avatar = serializers.URLField(
        source="user_avatar.user_avatar_url",
        required=False,
    )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "phone_number",
            "password",
            "profile",
            "date_joined",
            "is_employer",
            "is_employee",
            "is_two_factor_auth",
        ]
    id = serializers.IntegerField(required=False)
    email = serializers.CharField()
    phone_number = serializers.CharField()
    profile = ProfileSerializer(required=False)
    is_employer = serializers.BooleanField()
    is_employee = serializers.BooleanField()
    date_joined = serializers.DateTimeField(required=False)
    is_two_factor_auth = serializers.BooleanField(required=False)


class UserAvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAvatar
        fields = ["user_avatar_url"]
    user_avatar_url = serializers.FileField(write_only=True)


class TOTPTokenSerializer(serializers.Serializer):
    totp_token = serializers.CharField()


class PasswordFieldSerializer(serializers.Serializer):
    password = serializers.CharField()


class EmailFieldSerializer(serializers.Serializer):
    email = serializers.CharField()


class PhoneNumberFieldSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
