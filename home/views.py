from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from .forms import ContactForm, SigninForm
from django.core.mail import send_mail
from django.views import View
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
class HomeView(View):
    """user home view, allows you to send an email to ask a question"""
    def get(self, request):
        form = ContactForm(initial={'email': 'jojo@jojo.com'})
        return render(request, "home/index.html", {'form': form})

    def post(self, request):
        """the post method retrieves the information from the form, if valid, it uses django's mail library to send
        the visitor's message"""
        form = ContactForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            from_email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            from_name = form.cleaned_data['name']
            message = "expéditeur " + from_name + " mail: " + from_email + " tel: " + phone +\
                      " Demande: " + form.cleaned_data['message']
            subject = 'Renseignement AppOsteo'
            send_mail(subject, message, from_email, ['noritakasawamura84@gmail.com'])
            """use request.path to avoid form resending requests when refreshing the page"""
            return redirect(request.path)


class LoginAdminView(View):
    """view that handles admin login through a form"""
    def get(self, request):
        """the get method returns the login page with the form"""
        form = SigninForm()
        return render(request, "home/signin.html", {'form': form})

    def post(self, request):
        """the POST method retrieves information from the form. If there are and they are correct
        then the user is connected. If there is a next in the url then the user is redirected"""
        form = SigninForm(request.POST)
        message = ""
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['login'], password=form.cleaned_data['password']
            )
            if user is not None:
                login(request, user)
                obj = str(request.GET)
                if "next" in obj:
                    next_url = request.GET.get("next")
                    return redirect(next_url)
                else:
                    return redirect(settings.LOGIN_REDIRECT_URL)
            else:
                message = "Identifiants incorrects"
        return render(request, "home/signin.html", context={"message": message})


class LogoutAdminView(View):
    """User is disconnect and redirect on the login page"""
    def get(self, request):
        logout(request)
        return redirect("home-signin")


class HomeAdminView(LoginRequiredMixin, View):
    """admin homepage view uses the loginRequired mixin to verify that the user is authenticated
    before displaying the page. the view redirects to the planning page which is the central page for the
    practitioner"""
    def get(self, request):
        return redirect("fullcalendar")


class LegalView(TemplateView):
    """the LegalView uses a class based view TemplateView for displaying the legal notice template"""
    template_name = "home/legal_notice.html"
