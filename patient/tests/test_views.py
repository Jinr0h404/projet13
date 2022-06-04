import pytest

from django.urls import reverse
from django.test import Client
from django.core import mail
from django.test import TestCase
from patient.models import Patient
from pytest_django.asserts import assertTemplateUsed
from django.contrib.auth.models import User
from apposteo.tests.fixture_db_models import patient_fixture


@pytest.mark.django_db
class TestPatientViewClass():
    def test_PatientCreateView_view(self):
        """Creates a test client. Make a request on the URL retrieved using the reverse () function.
        Check that the HTTP status code is 302 if user not connected and 200 if user is connected.
        Check that the template used is the expected one"""
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
        response = client.post(path, {'last_name': "Tata",
                                      'first_name': "Tata",
                                      'birth_date': "1982-01-01",
                                      'phone': "0605253050",
                                      'street_number': 42,
                                      'street': 'rue de Paris',
                                      'zip_codde': 75500,
                                      'city': 'Paris'})
        new_count = Patient.objects.count()
        assert new_count == patient_number + 1
        assert response.status_code == 302


@pytest.mark.django_db(reset_sequences=True)
class TestManagePatientView():
    def test_ManagePatientView_get(self):
        """Creates a test client. Make a request on the URL retrieved using the reverse () function.
        Check that the HTTP status code is 200 if user is connected. Check that the template used
        is the expected one and check if the content of detail display is good"""
        client = Client()
        username = "test_user"
        password = "Troubadour"
        User.objects.create_superuser(username=username, password=password)
        client.login(username=username, password=password)
        response = client.get(reverse("patient", args=["1"]))
        expected_content = '<p class="masthead-subheading font-weight-light mb-0 text-left">' \
                           '<strong>Nom:</strong> Toto</p>'
        content = response.content.decode()

        assert expected_content in content
        assert response.status_code == 200
        assertTemplateUsed(response, 'patient/manage_patient.html')


@pytest.mark.django_db(reset_sequences=True)
class TestSearchPatientView():
    def test_SearcPatientView(self):
        client = Client()
        username = "test_user"
        password = "Troubadour"
        User.objects.create_superuser(username=username, password=password)
        client.login(username=username, password=password)
        path = reverse('search')
        response = client.get(path, {"query": "toto"})
        content = response.content.decode()
        expected_content = '<h3 class="lead text-white">Toto Toto né le 1 janvier 1980</h3>'

        assert expected_content in content
        assert response.status_code == 200
        assertTemplateUsed(response, 'patient/search_patient.html')

    def test_SearcPatientView_none(self):
        client = Client()
        username = "test_user"
        password = "Troubadour"
        User.objects.create_superuser(username=username, password=password)
        client.login(username=username, password=password)
        path = reverse('search')
        response = client.get(path, {"query": "tanos"})
        content = response.content.decode()
        expected_content = '<h3 class="lead text-white patient_not_found">Désolé, Vous n\'avez aucun patient de ce ' \
                           'nom ou prénom</h3>'

        assert expected_content in content
        assert response.status_code == 200
        assertTemplateUsed(response, 'patient/search_patient.html')
