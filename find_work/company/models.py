from uuid import uuid4

from django.db import models

from user.models import User


def company_avatar_url(
        instance,
        file,
):
    for_company = f"company_{instance.for_company.id}"
    dir_path = f"company_avatar/{for_company}"

    image_name, image_ext = file.split(".")
    unique_image_name = f"{image_name}-{uuid4()}.{image_ext}"

    file_path = f"{dir_path}/{unique_image_name}"
    return file_path


class Company(models.Model):
    author = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    name = models.CharField(
        max_length=150,
        unique=True
    )
    company_avatar = models.OneToOneField(
        "CompanyAvatar",
        on_delete=models.CASCADE,
        null=True,
    )
    is_delete = models.BooleanField(default=False)


class CompanyAvatar(models.Model):
    for_company = models.ForeignKey(
        "Company",
        on_delete=models.CASCADE
    )
    company_avatar_url = models.FileField(upload_to=company_avatar_url)
