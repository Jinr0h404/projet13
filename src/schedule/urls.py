from django.urls import path
from .views import ScheduleView, ScheduleCalendarView, ScheduleEditView, ScheduleChoiceView, ScheduleDeleteView


urlpatterns = [
    path('', ScheduleView.as_view(), name="shedule-planning"),
    path('fullcalendar/', ScheduleCalendarView.as_view(), name="fullcalendar"),
    path('fullcalendar/edit-<int:pk>/', ScheduleEditView.as_view(), name="edit-fullcalendar"),
    path('fullcalendar/choice/<int:pk>/<int:schedule>/', ScheduleChoiceView.as_view(), name="choice-fullcalendar"),
    path('fullcalendar/delete-<int:pk>/', ScheduleDeleteView.as_view(), name="delete-fullcalendar"),
]
