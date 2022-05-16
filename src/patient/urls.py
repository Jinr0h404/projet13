from django.urls import path
from .views import PatientCreateView, ManagePatientView, SearchPatientView


urlpatterns = [
    path('', PatientCreateView.as_view(), name="create-patient-index"),
    path('managepatient-<int:pk>/', ManagePatientView.as_view(), name="patient"),
    path('search/', SearchPatientView.as_view(), name="search"),
]
