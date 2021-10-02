import datetime
import logging
from django.apps import apps
from django import http
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DeleteView, UpdateView
from django.views.generic.detail import DetailView
from authorizations.models import Authorizations
from accounts.models import Profile
from .forms import AuthorizationForm, AuthorizationForm2
from trillian.models import Trillian


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


# def auth_create(request):
#    if request.method == 'POST':
#        form = AuthorizationForm2(request.POST)
#        if form.is_valid():


class AuthorizationCreate(LoginRequiredMixin, CreateView):
    model = Authorizations
    template_name = 'authorizations/authorization_create.html'
    success_url = reverse_lazy('accounts:profile')
    form_class = AuthorizationForm2

    def form_valid(self, form):
        form.instance.issuer_id = self.request.user.id
        log_service = apps.get_app_config('trillian').service_log
        # log_service = Trillian()
        print(f'{log_service}\n\n')
        profile = Profile.objects.get(user_id=self.request.user.id)
        token = form.data.get('token')
        try:
            data = log_service.decode_jwt(token=token, authorization_server_pk=profile.public_key)
            inclusion_proof, status_code = log_service.insert_jwt(data=data, token=token,
                                                                  authorization_server_pk=profile.public_key)
        except Exception as e:
            logging.exception(e)
            return http.HttpResponseBadRequest(f"Error: \n\n {e}")
        if status_code != 0:
            if inclusion_proof:
                print("Leaf already present in the log")
                print(inclusion_proof)
                return render(request=self.request, template_name='authorizations/inclusion_proof.html',
                              context={'inclusion_proof': inclusion_proof, 'status_code': status_code})
                # return http.HttpResponseRedirect(self.success_url)
            else:
                return http.HttpResponseBadRequest(f"Error in entering values. Status code:{status_code}")
        form.instance.client = data["client"]
        form.instance.server = data["server"]
        form.instance.start_validity = datetime.datetime.utcfromtimestamp(int(data["nbf"])). \
            strftime('%Y-%m-%d %H:%M')
        print(form.instance.start_validity)
        form.instance.expiration_time = datetime.datetime.utcfromtimestamp(int(data["exp"])). \
            strftime('%Y-%m-%d %H:%M')
        print(form.instance.expiration_time)
        form.instance.inclusion_proof = inclusion_proof
        print(form.instance.inclusion_proof)
        print(f"{form.instance}\n\n")
        self.object = form.save()
        return render(request=self.request, template_name='authorizations/inclusion_proof.html',
                      context={'inclusion_proof': inclusion_proof, 'status_code': status_code})


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


class InclusionProof(LoginRequiredMixin, ListView):
    model = Authorizations
    template_name = 'authorizations/inclusion_proof.html'

    def get(self, request, *args, **kwargs):
        object = Authorizations.objects.get(id=self.kwargs['pk'])
        print(object)
        return render(request=request, template_name=self.template_name, context={
            'inclusion_proof': object.inclusion_proof})
