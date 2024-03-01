from django.db import models


class Skill(models.Model):
    skill_name = models.CharField(
        max_length=150,
        unique=True
    )

    def __str__(self):
        return self.skill_name
