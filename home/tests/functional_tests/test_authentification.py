import pytest

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User
from django.urls import reverse
from selenium.webdriver.common.by import By
# import os


class TestAuthentification(StaticLiveServerTestCase):
    @pytest.mark.django_db(reset_sequences=True)
    def test_signin(self):
        """functional test with selenium to verify the user signin scenario."""
        # os.chmod('home/tests/functional_tests/chromedriver', 755)
        username = "test_user"
        password = "Troubadour"
        User.objects.create_superuser(username=username, password=password)
        # self.s = Service(executable_path="home/tests/functional_tests/chromedriver")
        # self.browser = webdriver.Chrome(service=self.s)
        # self.browser = webdriver.Chrome(ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        self.browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.browser.get(self.live_server_url + reverse("home-signin"))
        login = self.browser.find_element(By.ID, "login")
        login.send_keys("test_user")
        password = self.browser.find_element(By.ID, "password")
        password.send_keys("Troubadour")
        signin = self.browser.find_element(By.ID, "submitButton")
        signin.submit()
        self.assertEqual(
            self.browser.current_url, self.live_server_url + reverse("fullcalendar")
        )
        self.assertEqual(self.browser.find_element(By.TAG_NAME, "h2").text, "PLANNING")
        self.browser.close()
