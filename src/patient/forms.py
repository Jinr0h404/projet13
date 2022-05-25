from django import forms
from patient.models import Patient, Address, Attachment


class CreatePatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = [
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


class CreateAddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = [
            "street_number",
            "street",
            "zip_code",
            "city",
            "additional",
        ]


class UploadFileForm(forms.ModelForm):
    class Meta:
        model = Attachment
        fields = [
            "document_name",
            "document_join",
            "comment",
            "patient_unique_id"
        ]
