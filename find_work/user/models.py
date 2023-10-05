import random

from uuid import uuid4

from django.db import models
from django.contrib.auth.models import (
    PermissionsMixin,
    AbstractBaseUser,
    BaseUserManager,
)


def user_avatar_url(
        instance,
        file,
):
    file_name, file_ext = file.split(".")
    dir_path = f"user_avatar/user_{instance.profile.id}"
    file_path = f"{dir_path}/{file_name}-{uuid4()}.{file_ext}"
    return file_path


class Profile(models.Model):
    first_name = models.CharField(max_length=150)
    second_name = models.CharField(max_length=150)
    employer_profile = models.OneToOneField(
        "EmployerProfile",
        on_delete=models.CASCADE,
        null=True,
    )
    employee_profile = models.OneToOneField(
        "EmployeeProfile",
        on_delete=models.CASCADE,
        null=True,
    )
    user_avatar = models.OneToOneField(
        "UserAvatar",
        on_delete=models.CASCADE,
        null=True,
    )


class UserManager(BaseUserManager):
    def create_user(
        self,
        email,
        password,
    ):
        if email is None:
            raise TypeError("Users must have an email address.")

        profile = Profile(
            first_name="Helper",
            second_name="Helper",
            employer_profile=None,
            employee_profile=None,
        )

        profile.save()

        last_digits = str(random.random())[-10:]

        phone_number = f"000{last_digits}"

        user = self.model(
            email=self.normalize_email(email),
            profile=profile,
            phone_number=phone_number,
            is_employer=False,
            is_employee=False,
        )

        user.set_password(password)
        user.save()

        return user

    def create_superuser(
        self,
        email,
        password,
    ):
        if password is None:
            raise TypeError("Superusers must have a password.")

        user = self.create_user(
            email,
            password,
        )
        user.is_active = True
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(
    AbstractBaseUser,
    PermissionsMixin,
):
    email = models.EmailField(
        verbose_name="email",
        max_length=150,
        unique=True,
    )
    phone_number = models.TextField(unique=True)

    otp_base32 = models.CharField(
        max_length=200,
        null=True
    )
    user_activation_uuid = models.TextField()
    reset_password_uuid_hash = models.TextField(null=True)

    profile = models.OneToOneField(
        "Profile",
        on_delete=models.CASCADE,
    )
    date_joined = models.DateTimeField(
        verbose_name="date joined",
        auto_now_add=True,
    )
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_employer = models.BooleanField()
    is_employee = models.BooleanField()
    is_two_factor_auth = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"


class EmployerProfile(models.Model):
    projects_total = models.IntegerField(default=0)


class EmployeeProfile(models.Model):
    projects_compleat = models.IntegerField(default=0)


class UserAvatar(models.Model):
    user_avatar_url = models.FileField(upload_to=user_avatar_url)


# Create your models here.
