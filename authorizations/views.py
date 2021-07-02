from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView, CreateView, ListView
from django.views.generic.detail import DetailView
from authorizations.models import Authorizations
from .forms import AccountForm

# Create your views here.


class AuthorizationDetail(DetailView):
    model = Authorizations
    template_name = 'authorizations/authorization_detail.html'


class AuthorizationCreate(CreateView):
    model = Authorizations
    template_name = 'authorizations/authorization_create.html'
    success_url = reverse_lazy('homepage')
    form_class = AccountForm


class AuthorizationList(ListView):
    model = Authorizations
    template_name = 'authorizations/authorization_list.html'
