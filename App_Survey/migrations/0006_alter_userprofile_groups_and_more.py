# Generated by Django 5.1.1 on 2024-09-26 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App_Survey', '0005_alter_userprofile_groups_and_more'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='groups',
            field=models.ManyToManyField(related_name='app_auth_users_is_staff', to='auth.group'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user_permissions',
            field=models.ManyToManyField(related_name='app_auth_users_is_active', to='auth.permission'),
        ),
    ]
