from django import http
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DeleteView, UpdateView
from django.views.generic.detail import DetailView
from authorizations.models import Authorizations
from .forms import AuthorizationForm


# Create your views here.
class AuthorizationDetail(LoginRequiredMixin, DetailView):
    model = Authorizations
    template_name = 'authorizations/authorization_detail.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.issuer_id == request.user.pk:
            return render(request=request, template_name=self.template_name, context={'object': self.object})
        else:
            return http.HttpResponseForbidden("Cannot delete other's authorization")


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
    success_url = reverse_lazy('accounts:profile')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.issuer_id == request.user.pk:
            return render(request=request, template_name=self.template_name, context={'object': self.object})
        else:
            return http.HttpResponseForbidden("Cannot delete other's authorization")

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.issuer_id == request.user.pk:
            success_url = self.get_success_url()
            self.object.delete()
            return http.HttpResponseRedirect(success_url)
        else:
            return http.HttpResponseForbidden("Cannot delete other's authorization")


class AuthorizationUpdate(LoginRequiredMixin, UpdateView):
    model = Authorizations
    template_name = 'authorizations/authorization_update.html'
    success_url = reverse_lazy('accounts:profile')
    form_class = AuthorizationForm

    def form_valid(self, form):
        form.instance.issuer_id = self.request.user.id
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.issuer_id == request.user.pk:
            return render(request=request, template_name=self.template_name, context={'object': self.object,
                                                                                      'form': self.form_class(
                                                                                          instance=self.object)})
        else:
            return http.HttpResponseForbidden("Cannot update other's authorization")


class AuthorizationList(LoginRequiredMixin, ListView):
    model = Authorizations
    template_name = 'authorizations/authorization_list.html'
