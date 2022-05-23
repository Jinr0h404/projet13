from django import forms


class ContactForm(forms.Form):
    email = forms.EmailField(max_length=45, required=True)
    name = forms.CharField(min_length=3 ,max_length=45, required=True)
    phone = forms.CharField(max_length=10, required=True)
    message = forms.CharField(widget=forms.Textarea(),min_length=10, required=True)


class SigninForm(forms.Form):
    login = forms.CharField(max_length=10, required=True)
    password = forms.CharField(min_length=6, widget=forms.PasswordInput)