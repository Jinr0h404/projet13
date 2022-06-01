from django import forms
from .models import Price


class BillSessionForm(forms.Form):
    type_session = forms.ModelChoiceField(queryset=Price.objects.filter(id__lt=5).order_by('id'), initial=0)
