from django.db import models
from django.urls import reverse
# Create your models here.


class Address(models.Model):
    """this class is for the django orm, it gives the parameters for the
    creation of the table of the same name in the psql database."""
    street_number = models.IntegerField(blank=True)
    street = models.CharField(max_length=200, blank=True)
    zip_code = models.CharField(max_length=5, blank=True)
    city = models.CharField(max_length=150, blank=True)
    additional = models.CharField(max_length=200, blank=True)


class Patient(models.Model):
    """this class is for the django orm, it gives the parameters for the
    creation of the table of the same name in the psql database."""
    last_name = models.CharField(max_length=80, verbose_name="Nom", blank=False, null=False)
    first_name = models.CharField(max_length=80, verbose_name="Prenom", blank=False, null=False)
    birth_date = models.DateField(blank=False, null=False)
    mail = models.EmailField(max_length=300, blank=True)
    phone = models.CharField(max_length=20, verbose_name="Telephone", blank=False, null=False)
    job = models.CharField(max_length=150, verbose_name="Profession", blank=True, default="NC")
    glasses = models.BooleanField(blank=True, default="NC")
    medical_device = models.TextField(blank=True, default="NC")
    drug = models.TextField(blank=True, default="NC")
    pathology = models.TextField(blank=True, default="NC")
    comment = models.TextField(blank=True, default="NC")
    adresse_unique_id = models.ForeignKey(
        Address, on_delete=models.RESTRICT, verbose_name="Adresse", blank=True, null=True
    )

    def get_absolute_url(self):
        return reverse('patient', kwargs={'pk': self.pk})

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class Attachment(models.Model):
    """this class is for the django orm, it gives the parameters for the
    creation of the table of the same name in the psql database."""
    document_name = models.CharField(max_length=80, blank=False, null=False)
    document_join = models.FileField(upload_to=user_directory_path, null=False)
    comment = models.TextField(blank=True, default="NC")
    patient_unique_id = models.ForeignKey(
        Patient, on_delete=models.CASCADE, verbose_name="Piece jointe"
    )