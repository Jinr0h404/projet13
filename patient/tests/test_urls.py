import pytest
from django.urls import reverse, resolve


@pytest.mark.django_db(reset_sequences=True)
class TestPatientUrlClass:
    def test_patient_infos_url(self):
        path = reverse('patient', kwargs={'pk': 71})

        assert path == "/gestionosteo/patient/managepatient-71/"
        assert resolve(path).view_name == "patient"

    def test_session_infos_url(self):
        path = reverse('session-patient', kwargs={'pk': 1})

        assert path == "/gestionosteo/patient/session-1/"
        assert resolve(path).view_name == "session-patient"
