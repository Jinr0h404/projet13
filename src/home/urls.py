from django.urls import path
from .views import HomeView, LegalView


urlpatterns = [
    path('', HomeView.as_view(), name="home-index"),
    path('legal_notice', LegalView.as_view(), name="legal-notice"),
]
