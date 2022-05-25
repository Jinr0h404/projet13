import pytest
from django.urls import reverse, resolve
from apposteo.tests.test_models import patient_fixture


@pytest.mark.django_db
def test_patient_infos_url(patient_fixture):
    path = reverse('patient', kwargs={'pk': 1})

    assert path == "/gestionosteo/patient/managepatient-1/"
    assert resolve(path).view_name == "patient"
