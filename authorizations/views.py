from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView, CreateView, ListView, DeleteView
from django.views.generic.detail import DetailView
from authorizations.models import Authorizations
from .forms import AuthorizationForm

# Create your views here.


class AuthorizationDetail(LoginRequiredMixin, DetailView):
    model = Authorizations
    template_name = 'authorizations/authorization_detail.html'


class AuthorizationCreate(LoginRequiredMixin, CreateView):
    model = Authorizations
    template_name = 'authorizations/authorization_create.html'
    success_url = reverse_lazy('accounts:profile')
    form_class = AuthorizationForm

    def form_valid(self, form):
        form.instance.issuer_id = self.request.user.id
        return super().form_valid(form)


class AuthorizationDelete(LoginRequiredMixin, DeleteView):
    model = Authorizations
    template_name = 'authorizations/authorization_delete.html'
    success_url = reverse_lazy('authorizations:authorization_list')


class AuthorizationList(LoginRequiredMixin, ListView):
    model = Authorizations
    template_name = 'authorizations/authorization_list.html'
