from django.db import models


class WorkExperience(models.Model):
    work_experience_name = models.CharField(
        max_length=150,
    )

    def __str__(self):
        return self.work_experience_name
