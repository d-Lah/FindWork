# Generated by Django 4.2.1 on 2023-10-21 20:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_remove_user_two_factor_auth_hash_user_otp_base32'),
    ]

    operations = [
        migrations.AddField(
            model_name='useravatar',
            name='for_profile',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.profile'),
        ),
    ]
