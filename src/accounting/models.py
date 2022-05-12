from django.db import models
from schedule.models import Session


# Create your models here.
class Price(models.Model):
    """this class is for the django orm, it gives the parameters for the
    creation of the table of the same name in the psql database."""
    session_type = models.CharField(max_length=80, blank=False, null=False)
    price = models.IntegerField(blank=False)


class Bill(models.Model):
    """this class is for the django orm, it gives the parameters for the
    creation of the table of the same name in the psql database."""
    session_unique_id = models.ForeignKey(
        Session, on_delete=models.CASCADE
    )
    price_unique_id = models.ForeignKey(
        Price, on_delete=models.CASCADE
    )
