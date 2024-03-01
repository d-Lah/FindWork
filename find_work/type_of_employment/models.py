from django.db import models


class TypeOfEmployment(models.Model):
    type_of_employment_name = models.CharField(max_length=150)

    def __str__(self):
        return self.type_of_employment_name
