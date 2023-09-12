import random
from uuid import uuid4
from django.db import models
from django.contrib.auth.models import (
    PermissionsMixin,
    AbstractBaseUser,
    BaseUserManager
)

class Profile(models.Model):
    first_name = models.CharField(max_length=150)
    second_name = models.CharField(max_length=150)
    employee_profile = models.OneToOneField(
        "EmployeeProfile",
        on_delete=models.CASCADE,
        null=True
    )

class UserManager(BaseUserManager):
    def create_user(self, email, password):

        if email is None:
            raise TypeError('Users must have an email address.')

        profile = Profile(
            first_name="Helper",
            second_name="Helper"
        )

        profile.save()

        last_digits = str(random.random())[-10:]

        phone_number = f"super_user_{last_digits}"

        user = self.model(
            email=self.normalize_email(email),
            profile=profile,
            phone_number=phone_number
        )

        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password):

        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(
            email,
            password,
        )
        user.is_active = True
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user

class User(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(
        verbose_name="email",
        max_length=150,
        unique=True
    )
    phone_number = models.TextField(unique=True)

    user_activation_uuid = models.TextField()
    reset_passwor_uuid_hash = models.TextField(null=True)
    two_factor_auth_hash = models.TextField(null=True)

    profile = models.OneToOneField(
        "Profile",
        on_delete=models.CASCADE
    )
    date_joinded = models.DateTimeField(
        verbose_name="date joined",
        auto_now_add=True
    )
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_employer = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
    is_two_factor_auth = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

class EmployeeProfile(models.Model):
    work_experience = models.ManyToManyField("WorkExperience")
    knowledge_of_programming_language = models.ManyToManyField(
        "KnowledgeOfProgrammingLanguage"
    )

class WorkExperience(models.Model):
    experience = models.CharField(max_length=100)

    def __str__(self):
        return self.experience

class KnowledgeOfProgrammingLanguage(models.Model):
    programming_language = models.CharField(max_length=150)

    def __str__(self):
        return self.programming_language
# Create your models here.