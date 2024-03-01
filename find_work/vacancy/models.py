from django.db import models

from company.models import Company

from resume.models import Resume

from skill.models import Skill

from specialization.models import Specialization

from work_experience.models import WorkExperience

from type_of_employment.models import TypeOfEmployment


class Vacancy(models.Model):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=150)
    body = models.TextField()
    date_created = models.DateTimeField(
        verbose_name="date created",
        auto_now_add=True,
    )
    rqd_skill = models.ManyToManyField(
        Skill,
    )
    rqd_specialization = models.ForeignKey(
        Specialization,
        on_delete=models.CASCADE,
    )
    rqd_work_experience = models.ForeignKey(
        WorkExperience,
        on_delete=models.CASCADE,
    )
    rqd_type_of_employment = models.ManyToManyField(
        TypeOfEmployment,
    )
    is_close = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)
    resumes = models.ManyToManyField(
        Resume
    )
