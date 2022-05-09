from django.urls import path
from .views import PatientView, PatientCreateView

urlpatterns = [
    path('', PatientView.as_view(), name="patient-index"),
    path('create', PatientCreateView.as_view(), name="create-patient-index"),
]