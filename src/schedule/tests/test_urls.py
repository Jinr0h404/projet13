import pytest
from django.urls import reverse, resolve
from schedule.models import Session
from patient.models import Patient
from apposteo.tests.test_models import patient_fixture


@pytest.mark.django_db(reset_sequences=True)
def test_session_infos_url(patient_fixture):
    pk = Patient.objects.get(pk=1)
    Session.objects.create(reason="Mal de dos",
                           disease_history="chute dans les escaliers en 2020",
                           test="abductions des membres post",
                           action_summary="étirement de l'antéro postérieur",
                           patient_unique_id=pk)
    path = reverse('session-patient', kwargs={'pk': 1})

    assert path == "/gestionosteo/patient/session-1/"
    assert resolve(path).view_name == "session-patient"
