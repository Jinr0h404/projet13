# Generated by Django 4.0.4 on 2022-05-24 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0009_alter_attachment_document_join'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='glasses',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]
