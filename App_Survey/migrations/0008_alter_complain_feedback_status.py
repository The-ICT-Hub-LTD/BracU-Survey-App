# Generated by Django 5.1.1 on 2024-09-26 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App_Survey', '0007_alter_complain_feedback_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='complain',
            name='feedback_status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Solved', 'Solved'), ('On Process', 'On Process')], default='Pending', max_length=10),
        ),
    ]