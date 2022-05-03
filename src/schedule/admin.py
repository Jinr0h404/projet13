from django.contrib import admin

# Register your models here.
from .models import Planning, Session


admin.site.register(Planning)
admin.site.register(Session)