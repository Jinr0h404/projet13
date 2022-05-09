from django import forms
from patient.models import Patient

class CreatePatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields =[
            "mail",
            "last_name",
            "first_name",
            "phone",
            "birth_date",
            "job",
            "glasses",
            "medical_device",
            "drug",
            "pathology",
            "comment",
        ]