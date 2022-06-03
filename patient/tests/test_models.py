import pytest
from patient.models import user_directory_path, Attachment, Patient
from django.test import Client
from apposteo.tests.fixture_db_models import patient_fixture


@pytest.mark.django_db(reset_sequences=True)
def test_attachment_path_model(patient_fixture):
    join_doc = Attachment.objects.create(
               document_name="test_file",
               patient_unique_id=Patient.objects.get(pk=1))
    doc_join = user_directory_path(join_doc, 'test_file')
    expected_value = "user_Toto_Toto_1/test_file"
    assert doc_join == expected_value
