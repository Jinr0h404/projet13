import pytest
from patient.models import Patient


@pytest.fixture
def patient_fixture(db) -> Patient:
    Patient.objects.create(last_name="Toto",
                           first_name="Toto",
                           birth_date="1980-01-01",
                           phone="0605253050")