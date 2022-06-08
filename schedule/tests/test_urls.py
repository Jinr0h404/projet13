import pytest
from django.urls import reverse, resolve
from schedule.models import Session, Planning
from patient.models import Patient
from apposteo.tests.fixture_db_models import patient_fixture


@pytest.mark.django_db
def test_edit_calendar_url(patient_fixture):
    """Check if the name of the view is correct and that the URL matches the name of the view."""
    path = reverse('edit-fullcalendar', kwargs={'pk': 1})

    assert path == "/gestionosteo/schedule/fullcalendar/edit-1/"
    assert resolve(path).view_name == "edit-fullcalendar"


@pytest.mark.django_db
class TestScheduleUrlClass:
    def test_edit_calendar_url(self):
        """Check if the name of the view is correct and that the URL matches the name of the view."""
        path = reverse('edit-fullcalendar', kwargs={'pk': 1})

        assert path == "/gestionosteo/schedule/fullcalendar/edit-1/"
        assert resolve(path).view_name == "edit-fullcalendar"

    def test_delete_calendar_url(self):
        """Check if the name of the view is correct and that the URL matches the name of the view."""
        path = reverse('delete-fullcalendar', kwargs={'pk': 1})

        assert path == "/gestionosteo/schedule/fullcalendar/delete-1/"
        assert resolve(path).view_name == "delete-fullcalendar"

    def test_choice_calendar_url(self):
        """Check if the name of the view is correct and that the URL matches the name of the view."""
        path = reverse('choice-fullcalendar', kwargs={'pk': 1, 'schedule': 1})

        assert path == "/gestionosteo/schedule/fullcalendar/choice/1/1/"
        assert resolve(path).view_name == "choice-fullcalendar"

    def test_calendar_url(self):
        """Check if the name of the view is correct and that the URL matches the name of the view."""
        path = reverse('fullcalendar')

        assert path == "/gestionosteo/schedule/fullcalendar/"
        assert resolve(path).view_name == "fullcalendar"
