from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from .forms import CreatePatientForm, CreateAddressForm, UploadFileForm
from schedule.forms import CreateSessionForm
from schedule.models import Session
from .models import Patient, Address, Attachment
from django.views import View
from django.urls import reverse
from django.db.models import Q


# Create your views here.
class PatientCreateView(LoginRequiredMixin, View):
    """view that allows the creation of a patient, requires the connection of the admin account"""
    template_name = "patient/index_patient.html"
    model = Patient
    model_address = Address
    form_class = CreatePatientForm

    def get(self, request):
        """the get method will display two forms, the patient and the address."""
        form = CreatePatientForm()
        form_address = CreateAddressForm()
        return render(request, "patient/index_patient.html", {'form': form, 'form_address': form_address})

    def post(self, request):
        """the post method checks that the 2 forms are valid and if so,
        checks if a patient with the same first name and date of birth already exists. If not,
        the patient is created and the address is created after adding the new patient id."""
        form = CreatePatientForm(request.POST)
        form_address = CreateAddressForm(request.POST)
        if form.is_valid() and form_address.is_valid():
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


class ManagePatientView(LoginRequiredMixin, DetailView):
    """the patient management view using a class base detailview to retrieve information from the patient table
    and display it. It also allows the addition of attachments."""
    model = Patient
    context_object_name = "patient"
    template_name = "patient/manage_patient.html"

    def get_context_data(self, **kwargs):
        """the get_context_data method is used to add information from the address table and to display
        the new session form in the view template."""
        form = UploadFileForm()
        form_session = CreateSessionForm()
        context = super(ManagePatientView, self).get_context_data(**kwargs)
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
        """the post method retrieves the information from the add file form. If the form is valid,
        the element is created, the corresponding patient ID is added and the element is saved in the database."""
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.patient_unique_id = Patient.objects.get(pk=pk)
            document.save()
            return redirect('patient', pk)
        else:
            return redirect('patient', pk)


class SearchPatientView(LoginRequiredMixin, ListView):
    """the SearchPatientView view uses a class base listView to display the list of patients matching the search."""
    template_name = "patient/search_patient.html"
    model = Patient
    context_object_name = "patient"

    def get_queryset(self):
        """the get_queryset method retrieves the elements of the query. If there is an element then it searches in
        the list of users for matches of last name and / or first names. If there is a match, it returns the list
        of users found, otherwise the list of all users"""
        name = self.kwargs.get('query')
        name = self.request.GET.get('query')
        object_list = self.model.objects.all()
        if name:
            object_list = object_list.filter(Q(last_name__icontains=name) | Q(first_name__icontains=name))
        return object_list


class PatientUpdateView(LoginRequiredMixin, UpdateView):
    """the PatientUpdateView uses a view based on a class base updateView to update a patient's
    information in the db"""
    model = Patient
    template_name = "patient/edit_patient.html"
    form_class = CreatePatientForm

    def get_success_url(self):
        """the get_success_url method redirects the user to the patient management view after modification."""
        pk = self.kwargs["pk"]
        return reverse("patient", kwargs={"pk": pk})


class AddressUpdateView(LoginRequiredMixin, UpdateView):
    """the AddressUpdateView uses a view based on a class base updateView to update an address's
        information in the db"""
    model = Address
    template_name = "patient/edit_adress.html"
    form_class = CreateAddressForm

    def get_success_url(self):
        """the get_success_url method redirects the user to the patient management form after modification."""
        pk = self.kwargs["patient_pk"]
        return reverse("patient", kwargs={"pk": pk})


class AddressCreateView(LoginRequiredMixin, CreateView):
    """the AddressUpdateView uses a view based on a class base updateView to update an address's
        information in the db"""
    model = Address
    template_name = "patient/edit_adress.html"
    form_class = CreateAddressForm

    def form_valid(self, form):
        """the form_valid method retrieves the information from the form, checks the integrity on its own,
        adds the patient's id to the address and saves the element via the super() method"""
        pk = self.kwargs["patient_pk"]
        form.instance.patient_unique_id = Patient.objects.get(pk=pk)
        return super().form_valid(form)

    def get_success_url(self):
        """the get_success_url method redirects the user to the patient management form after modification."""
        pk = self.kwargs["patient_pk"]
        return reverse("patient", kwargs={"pk": pk})


class SessionPatientView(LoginRequiredMixin, DetailView):
    """the SessionPatientView view uses a class base DetailView to view details of a patient's selected session."""
    model = Session
    context_object_name = "session"
    template_name = "patient/session_patient.html"


class SessionCreateView(LoginRequiredMixin, CreateView):
    """the SessionCreateView view uses a class base CreateView to create a new patient's session."""
    model = Session
    template_name = "patient/manage_patient.html"
    form_class = CreateSessionForm

    def form_valid(self, form):
        """the form_valid method retrieves the information from the form, checks the integrity on its own,
        adds the patient's id to the session and saves the element via the super() method"""
        pk = self.kwargs["pk"]
        form.instance.patient_unique_id = Patient.objects.get(pk=pk)
        return super().form_valid(form)

    def get_success_url(self):
        """the get_success_url method redirects the user to the patient management view after modification."""
        pk = self.kwargs["pk"]
        return reverse("patient", kwargs={"pk": pk})
