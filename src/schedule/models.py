from django.db import models
from patient.models import Patient

# Create your models here.
class Planning(models.Model):
    """this class is for the django orm, it gives the parameters for the
    creation of the table of the same name in the psql database."""
    appointment_date = models.DateField(blank=False, null=False)
    appointment_hour = models.TimeField(blank=False, null=False)
    reason = models.CharField(max_length=200, blank=False)
    patient_name = models.CharField(max_length=80, blank=False)
    status = models.BooleanField(default=True)


class Session(models.Model):
    """this class is for the django orm, it gives the parameters for the
    creation of the table of the same name in the psql database."""
    appointment_date = models.DateField(blank=False, null=False)
    appointment_hour = models.TimeField(blank=False, null=False)
    reason = models.TextField(blank=False, null=False)
    action_summary = models.TextField(blank=True, default="NC")
    patient_unique_id = models.ForeignKey(
        Patient, on_delete=models.CASCADE
    )
    planning_unique_id = models.ForeignKey(
        Planning, on_delete=models.CASCADE
    )