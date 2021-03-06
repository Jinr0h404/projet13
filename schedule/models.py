# from django.utils import timezone
from django.db import models
from patient.models import Patient


# Create your models here.
class Planning(models.Model):
    """this class is for the django orm, it gives the parameters for the
    creation of the table of the same name in the psql database."""
    appointment_date_start = models.DateTimeField(blank=False, null=False)
    appointment_hour_stop = models.DateTimeField(blank=False, null=False)
    reason = models.CharField(max_length=200, blank=False)
    patient_unique_id = models.ForeignKey(
        Patient, on_delete=models.CASCADE, blank=True, null=True
    )


class Session(models.Model):
    """this class is for the django orm, it gives the parameters for the
    creation of the table of the same name in the psql database."""
    appointment_date = models.DateField(blank=False, null=False, auto_now_add=True)
    reason = models.TextField(blank=False, null=False)
    disease_history = models.TextField(blank=False, null=False, default="NC")
    test = models.TextField(blank=False, null=False, default="NC")
    action_summary = models.TextField(blank=True, default="NC")
    comment = models.TextField(blank=True, default="NC")
    patient_unique_id = models.ForeignKey(
        Patient, on_delete=models.CASCADE
    )
    planning_unique_id = models.ForeignKey(
        Planning, on_delete=models.CASCADE, blank=True, null=True
    )
