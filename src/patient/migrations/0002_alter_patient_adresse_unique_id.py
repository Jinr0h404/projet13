# Generated by Django 4.0.4 on 2022-04-30 10:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='adresse_unique_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='patient.address', verbose_name='Adresse'),
        ),
    ]