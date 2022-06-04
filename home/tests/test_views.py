import pytest

from django.urls import reverse
from django.test import Client
from django.core import mail
from django.test import TestCase
from pytest_django.asserts import assertTemplateUsed
from django.contrib.auth.models import User


@pytest.mark.django_db
class TestHomeViewClass():
    def test_HomeView_view(self):
        client = Client()
        path = reverse('home-index')
        response = client.get(path)
        content = response.content.decode()
        expected_content = '<p class="masthead-subheading font-weight-light mb-0">Tout savoir sur ' \
                           'l\'activité du cabinet</p>'

        assert expected_content in content
        assert response.status_code == 200
        assertTemplateUsed(response, "home/index.html")

    def test_LoginAdminView_view(self):
        client = Client()
        path = reverse('home-signin')
        response = client.get(path)
        content = response.content.decode()
        expected_content = '<p class="masthead-subheading font-weight-light mb-0">Se connecter pour accéder à la ' \
                           'gestion de vos rendez-vous</p>'

        assert expected_content in content
        assert response.status_code == 200
        assertTemplateUsed(response, "home/signin.html")

    def test_LoginAdminView_signin_view(self):
        client = Client()
        username = "test_user"
        password = "Troubadour"
        User.objects.create_superuser(username=username, password=password)
        path = reverse('home-signin')
        response = client.post(path, {'login': username, 'password': password})

        assert response.status_code == 302

    def test_LoginAdminView_bad_signin_view(self):
        client = Client()
        username = "test_user"
        password = "Troubadour"
        User.objects.create_superuser(username=username, password=password)
        path = reverse('home-signin')
        response = client.post(path, {'login': 'toto', 'password': password})
        content = response.content.decode()
        expected_content = '<p class="masthead-subheading text-center text-danger font-weight-light mb-0">' \
                           'Identifiants incorrects</p>'

        assert expected_content in content
        assert response.status_code == 200
        assertTemplateUsed(response, "home/signin.html")

    def test_LogoutAdminView_view(self):
        """Creates a test client. Make a request on the URL retrieved using the reverse () function.
        Check that the HTTP status code is 200 or the expected code. Check that the template used is the
        expected one"""
        client = Client()
        username = "test_user"
        password = "Troubadour"
        User.objects.create_superuser(username=username, password=password)
        client.login(username=username, password=password)
        path = reverse("home-signout")
        response = client.get(path)
        assert response.status_code == 302


class EmailTest(TestCase):
    def test_send_email(self):
        client = Client()
        path = reverse("home-index")
        response = client.post(path, {'email': 'toto@openclassrooms.com', 'name': 'Toto Dupond', 'phone': '0606060606',
                                      'message': 'Bonjour, que faire quand mal au dos?'})

        # Test that one message has been sent.
        self.assertEqual(len(mail.outbox), 1)
        # Verify that the subject of the first message is correct.
        self.assertEqual(mail.outbox[0].subject, 'Renseignement AppOsteo')
        self.assertEqual(response.status_code, 302)
