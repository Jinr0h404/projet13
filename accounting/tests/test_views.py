import pytest

from django.urls import reverse
from django.test import Client
from pytest_django.asserts import assertTemplateUsed
from schedule.models import Session
from patient.models import Patient
from apposteo.tests.fixture_db_models import patient_fixture


@pytest.mark.django_db
def test_BillPdfView_view(patient_fixture):
    client = Client()
    patient = Patient.objects.get(pk=1)
    Session.objects.create(appointment_date="10-06-2022",
                           reason="mal aux dents",
                           disease_history="est tombé dans les escaliers",
                           test="",
                           action_summary="",
                           comment="",
                           patient_unique_id=patient)
    path = reverse('create-session-bill', kwargs={'pk': 1})
    response = client.get(path)
    content = response.content.decode()
    expected_content = '<h1 class="masthead-heading text-uppercase mb-0 text-center">Facture</h1>'

    assert expected_content in content
    assert response.status_code == 200
    assertTemplateUsed(response, "accounting/session_bill.html")
