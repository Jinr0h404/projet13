from django import forms
from .models import Price


class BillSessionForm(forms.Form):
    """the BillSessionForm form class is used to create the drop-down list based on the Price model for the form
    for choosing the type of session in the edition of invoices"""
    type_session = forms.ModelChoiceField(queryset=Price.objects.filter(id__lt=5).order_by('id'), initial=0)
