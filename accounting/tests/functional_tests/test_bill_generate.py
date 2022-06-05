import pytest

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User
from django.urls import reverse
from selenium.webdriver.common.by import By
from patient.models import Patient, Address
from schedule.models import Session
from accounting.models import Price
import time


class TestBill(StaticLiveServerTestCase):
    @pytest.mark.django_db(reset_sequences=True)
    def test_bill_generate(self):
        """functional test with selenium to verify the user signin scenario."""
        username = "test_user"
        password = "Troubadour"
        User.objects.create_superuser(username=username, password=password)
        Patient.objects.create(last_name="Tartus",
                               first_name="Tortis",
                               birth_date="1970-01-01",
                               phone="0605253050")
        patient = Patient.objects.get(pk=2)
        Address.objects.create(street_number=42,
                               street="rue du test",
                               zip_code=50440,
                               city="Paris",
                               patient_unique_id=patient)
        Session.objects.create(appointment_date="2022-05-01 14:30:00+00:00",
                               reason="mal au dos",
                               disease_history="chute dans les escalier",
                               test="rotation sur les axes",
                               patient_unique_id=patient)
        Price.objects.create(session_type="session test",
                             price=45)
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        self.browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.browser.get(self.live_server_url + reverse("create-session-bill", kwargs={'pk': 2}))
        login = self.browser.find_element(By.ID, "login")
        login.send_keys("test_user")
        password = self.browser.find_element(By.ID, "password")
        password.send_keys("Troubadour")
        signin = self.browser.find_element(By.ID, "submitButton")
        signin.submit()
        time.sleep(5)
        edit = self.browser.find_element(By.ID, "submitButton")
        edit.click()
        self.assertEqual(
            self.browser.current_url, self.live_server_url + reverse("create-session-bill", kwargs={'pk': 2}))
        self.assertEqual(self.browser.find_element(By.TAG_NAME, "h1").text, "FACTURE")
        self.browser.close()
