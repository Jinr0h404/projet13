from django.urls import path
from .views import PatientCreateView, ManagePatientView, SearchPatientView, PatientUpdateView, AddressUpdateView,\
    SessionPatientView, SessionCreateView, AddressCreateView


urlpatterns = [
    path('', PatientCreateView.as_view(), name="create-patient-index"),
    path('managepatient-<int:pk>/', ManagePatientView.as_view(), name="patient"),
    path('search/', SearchPatientView.as_view(), name="search"),
    path('update-<int:pk>/', PatientUpdateView.as_view(), name="update-patient"),
    path('address-<int:patient_pk>/update-<int:pk>/', AddressUpdateView.as_view(), name="update-address"),
    path('address-<int:patient_pk>/create/', AddressCreateView.as_view(), name="create-address"),
    path('session-<int:pk>/', SessionPatientView.as_view(), name="session-patient"),
    path('create_session-<int:pk>/', SessionCreateView.as_view(), name="create_session-patient"),
]
