from django.db import models

from user.models import User

from skill.models import Skill

from specialization.models import Specialization

from work_experience.models import WorkExperience

from type_of_employment.models import TypeOfEmployment


class Resume(models.Model):
    author = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    about = models.TextField()
    specialization = models.ForeignKey(
        Specialization,
        on_delete=models.CASCADE,
    )
    skill = models.ManyToManyField(
        Skill,
    )
    work_experience = models.ForeignKey(
        WorkExperience,
        on_delete=models.CASCADE,
    )
    type_of_employment = models.ManyToManyField(
        TypeOfEmployment,
    )
    is_delete = models.BooleanField(default=False)
