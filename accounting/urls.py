from django.urls import path
from .views import BillPdfView

urlpatterns = [
    path('bill-<int:pk>/', BillPdfView.as_view(), name="create-session-bill"),
]
