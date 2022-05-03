from django.urls import path
from .views import ScheduleView, ScheduleCalendarView

urlpatterns = [
    path('', ScheduleView.as_view(), name="shedule-planning"),
    path('fullcalendar/', ScheduleCalendarView.as_view(), name="fullcalendar"),
]