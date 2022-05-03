from django.contrib import admin

# Register your models here.
from .models import Patient, Address


admin.site.register(Patient)
admin.site.register(Address)