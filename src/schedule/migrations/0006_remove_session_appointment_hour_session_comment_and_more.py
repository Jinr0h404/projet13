# Generated by Django 4.0.4 on 2022-05-22 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0005_alter_planning_patient_unique_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='session',
            name='appointment_hour',
        ),
        migrations.AddField(
            model_name='session',
            name='comment',
            field=models.TextField(blank=True, default='NC'),
        ),
        migrations.AddField(
            model_name='session',
            name='disease_history',
            field=models.TextField(default='NC'),
        ),
        migrations.AddField(
            model_name='session',
            name='test',
            field=models.TextField(default='NC'),
        ),
        migrations.AlterField(
            model_name='session',
            name='appointment_date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
