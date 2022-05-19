from django import forms
from .models import Planning


class CreateScheduleForm(forms.ModelForm):
    class Meta:
        model = Planning
        fields =[
            "appointment_date_start",
            "appointment_hour_stop",
            "reason",
        ]

class CreateInfoForm(forms.Form):
    last_name = forms.CharField(min_length=3, max_length=45, required=True)
    first_name = forms.CharField(min_length=3, max_length=45, required=True)
    phone = forms.CharField(max_length=10, required=True)