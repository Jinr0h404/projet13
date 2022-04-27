from django.shortcuts import render, redirect
from .forms import ContactForm, SigninForm
from django.core.mail import send_mail
from django.views import View
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
class HomeView(View):
    def get(self, request):
        form = ContactForm(initial={'email': 'jojo@jojo.com'})
        return render(request, "home/index.html", {'form': form})

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            from_email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            subject = 'Renseignement AppOsteo'
            send_mail(subject, message, from_email, ['noritakasawamura84@gmail.com'])
            """use request.path to avoid form resending requests when refreshing the page"""
            return redirect(request.path)


class LoginAdminView(View):
    def get(self, request):
        form = SigninForm()
        return render(request, "home/signin.html", {'form': form})

    def post(self, request):
        form = SigninForm(request.POST)
        message=""
        if form.is_valid():
            print(form.cleaned_data)
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
            #return redirect(settings.LOGIN_REDIRECT_URL)
        return render(request, "home/signin.html", context={"message": message})


class LogoutAdminView(View):
    """User is disconnect and redirect on the login page"""
    def get(self, request):
        logout(request)
        return redirect("home-signin")


class HomeAdminView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "home/index_admin.html")