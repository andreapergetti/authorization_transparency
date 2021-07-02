from django.contrib.auth.views import PasswordResetView
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView
from accounts.forms import RegisterForm


class UserCreateView(CreateView):
    form_class = RegisterForm
    template_name = 'accounts/user_create.html'
    success_url = reverse_lazy('homepage')


class ResetPasswordView(PasswordResetView):
    template_name = 'accounts/password_reset.html'
    success_url = reverse_lazy('accounts:password-reset-done')
