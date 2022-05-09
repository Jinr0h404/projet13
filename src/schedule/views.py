from django.shortcuts import render
from django.views import View
from .models import Planning
from datetime import datetime, timedelta
from django.http import HttpResponse
from django.views import generic
from django.utils.safestring import mark_safe
import calendar
import json
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import *


# Create your views here.
class ScheduleView(LoginRequiredMixin, View):
    template_name = "schedule/planning.html"


class ScheduleCalendarView(LoginRequiredMixin, View):
    def get(self, request):
        all_events = Planning.objects.all()
        event_arr = []
        for i in all_events:
            print(i.appointment_date_start.time())
            event_sub_arr = {}
            event_sub_arr['title'] = i.reason
            start_date = datetime.strptime(str(i.appointment_date_start.date()), "%Y-%m-%d").strftime("%Y-%m-%d")
            hour_start = datetime.strptime(str(i.appointment_date_start.time()), "%H:%M:%S").strftime("%H:%M:%S")
            hour_stop = datetime.strptime(str(i.appointment_hour_stop.time()),"%H:%M:%S").strftime("%H:%M:%S")
            print(hour_start)
            end_date = datetime.strptime(str(i.appointment_hour_stop.date()), "%Y-%m-%d").strftime("%Y-%m-%d")
            event_sub_arr['start'] = start_date+'T'+hour_start
            event_sub_arr['end'] = end_date+'T'+hour_stop
            event_arr.append(event_sub_arr)
        data = JsonResponse((event_arr), safe=False)
        datatest = json.dumps(event_arr)
            #return HttpResponse(json.dumps(event_arr), content_type='application/json'))
        #print(datatest, type(datatest))
        #return HttpResponse(json.dumps(event_arr))
        context = {
            "appointment": datatest
        }

        return render(request, "schedule/fullcalendar.html", context)