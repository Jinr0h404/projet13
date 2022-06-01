from django.contrib import admin
from .models import Patient, Address, Attachment
# Register your models here.


admin.site.register(Patient)
admin.site.register(Address)
admin.site.register(Attachment)
