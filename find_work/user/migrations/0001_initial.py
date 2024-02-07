# Generated by Django 4.2.1 on 2023-09-08 09:14

from django.db import (
    migrations,
    models,
)
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        (
            "auth",
            "0012_alter_user_first_name_max_length",
        ),
    ]

    operations = [
        migrations.CreateModel(
            name="EmployeeProfile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="KnowledgeOfProgrammingLanguage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "programming_language",
                    models.CharField(max_length=150),
                ),
            ],
        ),
        migrations.CreateModel(
            name="WorkExperience",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "experience",
                    models.CharField(max_length=100),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Profile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(max_length=150),
                ),
                (
                    "second_name",
                    models.CharField(max_length=150),
                ),
                (
                    "employee_profile",
                    models.OneToOneField(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="user.employeeprofile",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="employeeprofile",
            name="knowledge_of_programming_language",
            field=models.ManyToManyField(
                to="user.knowledgeofprogramminglanguage"
            ),
        ),
        migrations.AddField(
            model_name="employeeprofile",
            name="work_experience",
            field=models.ManyToManyField(to="user.workexperience"),
        ),
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "password",
                    models.CharField(
                        max_length=128,
                        verbose_name="password",
                    ),
                ),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True,
                        null=True,
                        verbose_name="last login",
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        max_length=150,
                        unique=True,
                        verbose_name="email",
                    ),
                ),
                (
                    "phone_number",
                    models.TextField(),
                ),
                (
                    "user_activation_uuid",
                    models.TextField(),
                ),
                (
                    "reset_passwor_uuid_hash",
                    models.TextField(null=True),
                ),
                (
                    "two_factor_auth_hash",
                    models.TextField(null=True),
                ),
                (
                    "date_joinded",
                    models.DateTimeField(
                        auto_now_add=True,
                        verbose_name="date joined",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(default=False),
                ),
                (
                    "is_admin",
                    models.BooleanField(default=False),
                ),
                (
                    "is_staff",
                    models.BooleanField(default=False),
                ),
                (
                    "is_superuser",
                    models.BooleanField(default=False),
                ),
                (
                    "is_employer",
                    models.BooleanField(default=False),
                ),
                (
                    "is_employee",
                    models.BooleanField(default=False),
                ),
                (
                    "is_two_factor_auth",
                    models.BooleanField(default=False),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "profile",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="user.profile",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
