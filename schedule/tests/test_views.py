import pytest

from django.urls import reverse
from django.test import Client
from schedule.models import Planning
from patient.models import Patient
from pytest_django.asserts import assertTemplateUsed
from django.contrib.auth.models import User


@pytest.mark.django_db(reset_sequences=True)
class TestScheduleViewClass():
    def test_ScheduleCalendarView_view(self):
        client = Client()
        username = "test_user"
        password = "Troubadour"
        User.objects.create_superuser(username=username, password=password)
        client.login(username=username, password=password)
        Patient.objects.create(last_name="Titus",
                               first_name="Titus",
                               birth_date="1970-01-01",
                               phone="0605253050")
        patient = Patient.objects.get(pk=1)
        Planning.objects.create(appointment_date_start="2022-05-01 14:30:00+00:00",
                                appointment_hour_stop="2022-05-01 15:30:00+00:00",
                                reason="Douleur lombaire",
                                patient_unique_id=patient)
        path = reverse('fullcalendar')
        response = client.get(path)
        content = response.content.decode()
        expected_content = '<h2 class="page-section-heading text-center text-uppercase text-secondary mb-0">' \
                           'Planning</h2>'

        assert expected_content in content
        assert response.status_code == 200
        assertTemplateUsed(response, "schedule/fullcalendar.html")

    def test_ScheduleCalendarView_post_view(self):
        client = Client()
        username = "test_user"
        password = "Troubadour"
        User.objects.create_superuser(username=username, password=password)
        client.login(username=username, password=password)
        patient_number = Patient.objects.count()
        schedule_number = Planning.objects.count()
        path = reverse('fullcalendar')
        response = client.post(path, {'last_name': "Tata",
                                      'first_name': "Tata",
                                      'birth_date': "1982-01-01",
                                      'phone': "0605253050",
                                      'appointment_date_start': '2022-06-01 19:30:00+00:00',
                                      'appointment_hour_stop': '2022-06-01 20:30:00+00:00',
                                      'reason': 'mal au dos'})

        new_count = Patient.objects.count()
        new_chedule_count = Planning.objects.count()
        assert new_count == patient_number + 1
        assert new_chedule_count == schedule_number + 1
        assert response.status_code == 302
