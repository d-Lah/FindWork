from django.db import models


class Specialization(models.Model):
    specialization_name = models.CharField(
        max_length=150,
        unique=True
    )

    def __str__(self):
        return self.specialization_name
