from django.db import models
from user.models import User


class Resume(models.Model):
    author = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    about = models.TextField()
    specialization = models.ForeignKey(
        "Specialization",
        on_delete=models.CASCADE
    )
    skill = models.ManyToManyField(
        "Skill",
    )
    work_experience = models.ForeignKey(
        "WorkExperience",
        on_delete=models.CASCADE
    )
    type_of_employment = models.ManyToManyField(
        "TypeOfEmployment",
    )
    is_delete = models.BooleanField(default=False)


class Specialization(models.Model):
    specialization_name = models.CharField(
        max_length=150,
        unique=True
    )


class Skill(models.Model):
    skill_name = models.CharField(
        max_length=150,
        unique=True
    )


class WorkExperience(models.Model):
    work_experience_name = models.CharField(
        max_length=150,
    )


class TypeOfEmployment(models.Model):
    type_of_employment_name = models.CharField(max_length=150)
