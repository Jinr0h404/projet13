import pytest

from django.urls import reverse
from django.test import Client
from pytest_django.asserts import assertTemplateUsed
from schedule.models import Session
from patient.models import Patient
from django.contrib.auth.models import User
from apposteo.tests.fixture_db_models import patient_fixture


@pytest.mark.django_db(reset_sequences=True)
def test_BillPdfView_view(patient_fixture):
    """Create a test client. Query the retrieved URL using the reverse() function. Checks that the HTTP
    status code is 200 or the expected code. Checks that the model used is the one expected. Verifies that
    the content of the html corresponds to that expected"""
    client = Client()
    username = "test_user"
    password = "Troubadour"
    User.objects.create_superuser(username=username, password=password)
    client.login(username=username, password=password)
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
