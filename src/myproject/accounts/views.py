"""Account views — login, logout, profile."""
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from .forms import LoginForm


class LoginView(auth_views.LoginView):
    template_name = "registration/login.html"
    authentication_form = LoginForm


class LogoutView(auth_views.LogoutView):
    template_name = "registration/logout.html"


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "registration/profile.html"
