# Generated by Django 5.1.1 on 2024-10-06 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App_Survey', '0007_alter_complain_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='complain',
            name='is_feedback',
            field=models.BooleanField(default=False),
        ),
    ]