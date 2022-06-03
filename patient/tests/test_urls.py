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

    def test_search_patient_url(self):
        path = reverse('search')

        assert path == "/gestionosteo/patient/search/"
        assert resolve(path).view_name == "search"

    def test_update_patient_url(self):
        path = reverse('update-patient', kwargs={'pk': 1})

        assert path == "/gestionosteo/patient/update-1/"
        assert resolve(path).view_name == "update-patient"

    def test_update_address_patient_url(self):
        path = reverse('update-address', kwargs={'patient_pk': 1, 'pk': 1})

        assert path == "/gestionosteo/patient/address-1/update-1/"
        assert resolve(path).view_name == "update-address"

    def test_create_session_patient_url(self):
        path = reverse('create_session-patient', kwargs={'pk': 1})

        assert path == "/gestionosteo/patient/create_session-1/"
        assert resolve(path).view_name == "create_session-patient"
