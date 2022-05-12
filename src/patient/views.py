from django.shortcuts import render, redirect
from django.views.generic import CreateView, TemplateView, DetailView, ListView
from home.forms import ContactForm
from .forms import CreatePatientForm
from .models import Patient, Address
from django.core.mail import send_mail
from django.views import View
from django.urls import reverse_lazy


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


class PatientCreateView(CreateView):
    template_name = "patient/index_patient.html"
    model = Patient
    model_address = Address
    # fields = ['last_name', 'first_name', 'mail', 'birth_date', 'phone', 'job', 'glasses', 'medical_device', 'drug', 'pathology', 'comment']
    form_class = CreatePatientForm

    def form_valid(self, form):
        return super().form_valid(form)


class ManagePatientView(DetailView):
    model = Patient
    context_object_name = "patient"
    template_name = "patient/manage_patient.html"


class SearchPatientView(ListView):
    template_name = "patient/search_patient.html"
    model = Patient
    context_object_name = "patient"

    def get_queryset(self):
        name = self.kwargs.get('query')
        print(name)
        name = self.request.GET.get('query')
        print(name)
        object_list = self.model.objects.all()
        print(name)
        if name:
            object_list = object_list.filter(last_name__icontains=name)
        return object_list
