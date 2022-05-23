from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, UpdateView, DeleteView
from .models import Planning
from datetime import datetime, timedelta
import calendar
import json
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from patient.models import Patient
from patient.forms import CreatePatientForm
from .forms import CreateScheduleForm, CreateInfoForm
from django.db.models import Q

# Create your views here.
class ScheduleView(LoginRequiredMixin, TemplateView):
    template_name = "schedule/planning.html"


class ScheduleCalendarView(LoginRequiredMixin, View):
    def get(self, request):
        form = CreateScheduleForm()
        form_info = CreateInfoForm()
        all_events = Planning.objects.all()
        event_arr = []
        for i in all_events:
            print(i.appointment_date_start.time())
            event_sub_arr = {}
            event_sub_arr['title'] = i.reason
            start_date = datetime.strptime(str(i.appointment_date_start.date()), "%Y-%m-%d").strftime("%Y-%m-%d")
            hour_start = datetime.strptime(str(i.appointment_date_start.time()), "%H:%M:%S").strftime("%H:%M:%S")
            hour_stop = datetime.strptime(str(i.appointment_hour_stop.time()), "%H:%M:%S").strftime("%H:%M:%S")
            print(hour_start)
            end_date = datetime.strptime(str(i.appointment_hour_stop.date()), "%Y-%m-%d").strftime("%Y-%m-%d")
            event_sub_arr['start'] = start_date+'T'+hour_start
            event_sub_arr['end'] = end_date+'T'+hour_stop
            #event_sub_arr['url'] = "/gestionosteo/patient/managepatient-" + str(i.patient_unique_id_id)
            event_sub_arr['url'] = "/gestionosteo/schedule/fullcalendar/choice" + "/" + str(i.patient_unique_id_id) + "/" +str(i.id) + "/"
            event_arr.append(event_sub_arr)
        data = JsonResponse((event_arr), safe=False)
        datatest = json.dumps(event_arr)
            # return HttpResponse(json.dumps(event_arr), content_type='application/json'))
        # print(datatest, type(datatest))
        # return HttpResponse(json.dumps(event_arr))
        context = {
            "appointment": datatest,
            'form': form,
            'form_info': form_info
        }

        return render(request, "schedule/fullcalendar.html", context)

    def post(self, request):
        form = CreateScheduleForm(request.POST)
        form_info = CreatePatientForm(request.POST)
        if form.is_valid() and form_info.is_valid():
            """use request.path to avoid form resending requests when refreshing the page"""
            schedule = form.save(commit=False)
            schedule_info = form_info.save(commit=False)
            patient_lastname = Q(last_name__contains=schedule_info.last_name)
            patient_firstname = Q(first_name__contains=schedule_info.first_name)
            patient_birth = Q(birth_date__contains=schedule_info.birth_date)
            q =  Patient.objects.filter(patient_lastname & patient_firstname & patient_birth)
            if q:
                schedule.patient_unique_id = q[0]
            else:
                schedule_info.save()
                patient_lastname = Q(last_name__contains=schedule_info.last_name)
                patient_firstname = Q(first_name__contains=schedule_info.first_name)
                patient_birth = Q(birth_date__contains=schedule_info.birth_date)
                q = Patient.objects.filter(patient_lastname & patient_firstname & patient_birth)
                schedule.patient_unique_id = q[0]
            schedule.reason = schedule.reason + " " + schedule_info.last_name + " " + schedule_info.first_name + " " + str(schedule_info.birth_date) + " " + schedule_info.phone
            schedule.save()
            return redirect(request.path)
        else:
            return render(request, "schedule/fullcalendar.html")


class ScheduleEditView(LoginRequiredMixin, UpdateView):
    model = Planning
    template_name = "schedule/edit_fullcalendar.html"
    fields = ['reason', 'appointment_date_start', 'appointment_hour_stop']
    success_url = reverse_lazy("fullcalendar")

class ScheduleDeleteView(LoginRequiredMixin, DeleteView):
    model = Planning
    template_name = "schedule/delete_fullcalendar.html"
    success_url = reverse_lazy("fullcalendar")


class ScheduleChoiceView(LoginRequiredMixin, View):
    template_name = "schedule/choice_event_calendar.html"
    def get(self, request, pk, schedule):
        context = {"patient_id" : pk, "event_id": schedule}
        return render(request, "schedule/choice_event_calendar.html", context)
