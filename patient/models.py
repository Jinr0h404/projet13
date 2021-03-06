from django.db import models
from django.urls import reverse
# Create your models here.


class Patient(models.Model):
    """this class is for the django orm, it gives the parameters for the
    creation of the table of the same name in the psql database."""
    last_name = models.CharField(max_length=80, verbose_name="Nom", blank=False, null=False)
    first_name = models.CharField(max_length=80, verbose_name="Prenom", blank=False, null=False)
    birth_date = models.DateField(blank=False, verbose_name="Date de naissance", null=False)
    mail = models.EmailField(max_length=300, verbose_name="Adresse email", blank=True)
    phone = models.CharField(max_length=20, verbose_name="Telephone", blank=False, null=False)
    job = models.CharField(max_length=150, verbose_name="Profession", blank=True, default="NC")
    glasses = models.BooleanField(blank=True, verbose_name="Dispositif correctif de vision", default=False)
    medical_device = models.TextField(blank=True, verbose_name="Dispositif médical", default="NC")
    drug = models.TextField(blank=True, verbose_name="Traitement en cours", default="NC")
    pathology = models.TextField(blank=True, verbose_name="Pathologie", default="NC")
    comment = models.TextField(blank=True, verbose_name="Commentaire", default="NC")

    def get_absolute_url(self):
        return reverse('patient', kwargs={'pk': self.pk})


def user_directory_path(instance, filename):
    """This function allows you to define the path for saving attachments.
    It is called by the attachment table with the upload_to attribute.
    file will be uploaded to MEDIA_ROOT/user_<id>/<filename>"""
    patient_name = instance.patient_unique_id
    return 'user_{0}_{1}_{2}/{3}'.format(
        patient_name.last_name,
        patient_name.first_name,
        patient_name.id,
        filename)


class Attachment(models.Model):
    """this class is for the django orm, it gives the parameters for the
    creation of the table of the same name in the psql database."""
    document_name = models.CharField(max_length=80, blank=False, null=False)
    document_join = models.FileField(upload_to=user_directory_path, blank=True, null=True)
    comment = models.TextField(blank=True, default="NC")
    patient_unique_id = models.ForeignKey(
        Patient, on_delete=models.CASCADE, verbose_name="Patient Piece jointe", blank=True, null=True
    )


class Address(models.Model):
    """this class is for the django orm, it gives the parameters for the
    creation of the table of the same name in the psql database."""
    street_number = models.IntegerField(verbose_name="numéro", blank=True)
    street = models.CharField(max_length=200, verbose_name="nom de rue", blank=True)
    zip_code = models.CharField(max_length=5, verbose_name="code postal", blank=True)
    city = models.CharField(max_length=150, verbose_name="ville", blank=True)
    additional = models.CharField(max_length=200, verbose_name="complément", blank=True)
    patient_unique_id = models.ForeignKey(
        Patient, on_delete=models.CASCADE, verbose_name="patient", blank=True, null=True
    )
