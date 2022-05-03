from django.shortcuts import render, redirect
from home.forms import ContactForm
from django.core.mail import send_mail
from django.views import View

# Create your views here.
class PatientView(View):
    def get(self, request):
        form = ContactForm(initial={'email': 'jojo@jojo.com'})
        return render(request, "patient/index_patient.html", {'form': form})

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            from_email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            subject = 'Renseignement AppOsteo'
            send_mail(subject, message, from_email, ['noritakasawamura84@gmail.com'])
            """use request.path to avoid form resending requests when refreshing the page"""
            return redirect(request.path)
