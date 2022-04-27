from django.contrib import admin

# Register your models here.
from .models import Price, Bill


admin.site.register(Price)
admin.site.register(Bill)