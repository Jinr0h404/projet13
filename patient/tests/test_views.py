import pytest

from django.urls import reverse
from django.test import Client
from django.core import mail
from django.test import TestCase
from patient.models import Patient
from pytest_django.asserts import assertTemplateUsed
from django.contrib.auth.models import User


@pytest.mark.django_db
class TestPatientViewClass():
    def test_PatientCreateView_view(self):
        client = Client()
        path = reverse('create-patient-index')
        response = client.get(path)
        if response.status_code == 302:
            username = "test_user"
            password = "Troubadour"
            User.objects.create_superuser(username=username, password=password)
            client.login(username=username, password=password)
            new_response = client.get(path)
            content = new_response.content.decode()
            expected_content = '<p class="masthead-subheading font-weight-light mb-0">Gérer vos patients</p>'

            assert expected_content in content
            assert new_response.status_code == 200
            assertTemplateUsed(new_response, "patient/index_patient.html")

    def test_PatientCreateView_post_view(self):
        """Creates a test client. Make a post request on the URL retrieved using the reverse () function.
        also tests the model by checking that the patient is added in the db. Check that the HTTP status
        code is 302 due to the redirect."""
        client = Client()
        username = "test_user"
        password = "Troubadour"
        User.objects.create_superuser(username=username, password=password)
        client.login(username=username, password=password)
        patient_number = Patient.objects.count()
        path = reverse('create-patient-index')
        response = client.post(path, {'last_name': "Toto",
                                      'first_name': "Toto",
                                      'birth_date': "1980-01-01",
                                      'phone': "0605253050",
                                      'street_number': 42,
                                      'street': 'rue de Paris',
                                      'zip_codde': 75500,
                                      'city': 'Paris'})
        new_count = Patient.objects.count()
        assert new_count == patient_number + 1
        assert response.status_code == 302
