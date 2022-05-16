from django.shortcuts import render, redirect
from django.views.generic import CreateView, TemplateView, DetailView, ListView
from home.forms import ContactForm
from .forms import CreatePatientForm, CreateAddressForm
from .models import Patient, Address
from django.core.mail import send_mail
from django.views import View
from django.urls import reverse_lazy, reverse
from django.db.models import Q


# Create your views here.
class PatientCreateView(View):
    template_name = "patient/index_patient.html"
    model = Patient
    model_address = Address
    form_class = CreatePatientForm

    def get(self, request):
        form = CreatePatientForm()
        form_address = CreateAddressForm()
        return render(request, "patient/index_patient.html", {'form': form, 'form_address': form_address})

    def post(self, request):
        form = CreatePatientForm(request.POST)
        form_address = CreateAddressForm(request.POST)
        if form.is_valid() and form_address.is_valid():
            print(form.cleaned_data)
            print(form_address.cleaned_data)
            """use request.path to avoid form resending requests when refreshing the page"""
            patient = form.save(commit=False)
            patient_lastname = Q(last_name__contains=patient.last_name)
            patient_firstname = Q(first_name__contains=patient.first_name)
            patient_birth = Q(birth_date__contains=patient.birth_date)
            q =  Patient.objects.filter(patient_lastname & patient_firstname & patient_birth)
            if q:
                return redirect(reverse("search") + '?query=' + patient.last_name)
            else:
                patient.save()
                address = form_address.save(commit=False)
                address.patient_unique_id = patient
                address.save()
                return redirect('patient', patient.pk)


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
            print(name)
            object_list = object_list.filter(Q(last_name__icontains=name) | Q(first_name__icontains=name))
        return object_list
