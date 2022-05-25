from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from .forms import CreatePatientForm, CreateAddressForm, UploadFileForm
from schedule.forms import CreateSessionForm
from schedule.models import Session
from .models import Patient, Address, Attachment
from django.core.mail import send_mail
from django.views import View
from django.urls import reverse
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
        print(form)
        if form.is_valid() and form_address.is_valid():
            print(form.cleaned_data)
            print(form_address.cleaned_data)
            """use request.path to avoid form resending requests when refreshing the page"""
            patient = form.save(commit=False)
            patient_lastname = Q(last_name__contains=patient.last_name)
            patient_firstname = Q(first_name__contains=patient.first_name)
            patient_birth = Q(birth_date__contains=patient.birth_date)
            q = Patient.objects.filter(patient_lastname & patient_firstname & patient_birth)
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

    def get_context_data(self, **kwargs):
        form = UploadFileForm()
        form_session = CreateSessionForm()
        # Call the base implementation first to get a context
        context = super(ManagePatientView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the address
        address_detail = Address.objects.filter(patient_unique_id=self.kwargs['pk'])
        session_list = Session.objects.filter(patient_unique_id=self.kwargs['pk'])
        file_list = Attachment.objects.filter(patient_unique_id=self.kwargs['pk'])
        context['address'] = address_detail
        context['session_list'] = session_list
        context['file_list'] = file_list
        context['form'] = form
        context['form_session'] = form_session
        return context

    def post(self, request, pk):
        form = UploadFileForm(request.POST, request.FILES)
        # form_session = CreateSessionForm(request.POST)
        if form.is_valid():
            document = form.save(commit=False)
            document.patient_unique_id = Patient.objects.get(pk=pk)
            document.save()
            return redirect('patient', pk)
        else:
            return redirect('patient', pk)


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


class PatientUpdateView(LoginRequiredMixin, UpdateView):
    model = Patient
    template_name = "patient/edit_patient.html"
    # fields = ['reason', 'appointment_date_start', 'appointment_hour_stop']
    form_class = CreatePatientForm

    def get_success_url(self):
        pk = self.kwargs["pk"]
        return reverse("patient", kwargs={"pk": pk})


class AddressUpdateView(LoginRequiredMixin, UpdateView):
    model = Address
    template_name = "patient/edit_adress.html"
    # fields = ['reason', 'appointment_date_start', 'appointment_hour_stop']
    form_class = CreateAddressForm

    def get_success_url(self):
        pk = self.kwargs["patient_pk"]
        return reverse("patient", kwargs={"pk": pk})


class SessionPatientView(DetailView):
    model = Session
    context_object_name = "session"
    template_name = "patient/session_patient.html"


class SessionCreateView(LoginRequiredMixin, CreateView):
    model = Session
    template_name = "patient/edit_patient.html"
    form_class = CreateSessionForm

    def form_valid(self, form):
        pk = self.kwargs["pk"]
        form.instance.patient_unique_id = Patient.objects.get(pk=pk)
        return super().form_valid(form)

    def get_success_url(self):
        pk = self.kwargs["pk"]
        return reverse("patient", kwargs={"pk": pk})
