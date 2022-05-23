from django.contrib import admin

# Register your models here.
from .models import Patient, Address, Attachment


admin.site.register(Patient)
admin.site.register(Address)
admin.site.register(Attachment)