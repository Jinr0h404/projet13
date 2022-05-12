from django.urls import path
from .views import PatientView, PatientCreateView, ManagePatientView, SearchPatientView


urlpatterns = [
    path('', PatientView.as_view(), name="patient-index"),
    path('create', PatientCreateView.as_view(), name="create-patient-index"),
    path('managepatient-<int:pk>/', ManagePatientView.as_view(), name="patient"),
    path('search/', SearchPatientView.as_view(), name="search"),
]
