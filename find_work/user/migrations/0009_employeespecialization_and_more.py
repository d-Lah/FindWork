# Generated by Django 4.2.1 on 2024-01-07 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_remove_user_reset_password_uuid_hash'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmployeeSpecialization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
            ],
        ),
        migrations.AddField(
            model_name='employeeprofile',
            name='specialization',
            field=models.ManyToManyField(to='user.employeespecialization'),
        ),
    ]
