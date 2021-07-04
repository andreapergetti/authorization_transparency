from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView, CreateView, ListView, DeleteView
from django.views.generic.detail import DetailView
from authorizations.models import Authorizations
from .forms import AuthorizationForm

# Create your views here.


class AuthorizationDetail(DetailView):
    model = Authorizations
    template_name = 'authorizations/authorization_detail.html'


class AuthorizationCreate(CreateView):
    model = Authorizations
    template_name = 'authorizations/authorization_create.html'
    success_url = reverse_lazy('homepage')
    form_class = AuthorizationForm


class AuthorizationDelete(DeleteView):
    model = Authorizations
    template_name = 'authorizations/authorization_delete.html'
    success_url = reverse_lazy('authorizations:authorization_list')


class AuthorizationList(ListView):
    model = Authorizations
    template_name = 'authorizations/authorization_list.html'
