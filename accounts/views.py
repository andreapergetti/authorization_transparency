from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordResetView
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count
from django.db.models.functions import TruncDay
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
import datetime
import json

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from accounts.forms import RegisterForm, EmailChangeForm, PublicKeyChangeForm
from authorizations.models import Authorizations, Profile


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.public_key = form.cleaned_data.get('public_key')
            user.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('homepage')
    else:
        form = RegisterForm()
    return render(request, 'accounts/user_create.html', {'form': form})


@login_required() 
def email_change(request):
#    form = EmailChangeForm()
    if request.method == 'POST':
        form = EmailChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/accounts/profile/")
    else:
        form = EmailChangeForm(request.user)
    return render(request, 'accounts/email_change.html', {'form': form})
#        return render_to_response("email_change.html", {'form':form},
#                                  context_instance=RequestContext(request))

@login_required() 
def public_key_change(request):
#    form = PublicKeyChangeForm()
    if request.method == 'POST':
        form = PublicKeyChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/accounts/profile/")
    else:
        form = PublicKeyChangeForm(request.user)
        return render(request, 'accounts/public_key_change.html', {'form': form})
#        return render_to_response("email_change.html", {'form':form},
#                                  context_instance=RequestContext(request))


class ResetPasswordView(PasswordResetView):
    template_name = 'accounts/password_reset.html'
    success_url = reverse_lazy('accounts:password_reset_done')
    email_template_name = 'accounts/password_reset_email.html'


#class SelectObjectProfile(ListView):
#    template_name = 'accounts/profile_select_delete.html'
#    success_url = reverse_lazy('authorizations:authorization_delete')

#    def get_queryset(self):
#        queryset = Authorizations.objects.filter(issuer=self.request.user.id)
#        return queryset


def select_object_delete(request):
    if request.method == 'POST':
        print(request.POST)
        auth_id = request.POST.get('id', False)
        if auth_id:
            return redirect('authorizations:authorization_delete', pk=auth_id)
        else:
            queryset = Authorizations.objects.filter(issuer=request.user.id)
            context = {
                'object_list': queryset
            }
            return render(request=request, template_name='accounts/profile_select_delete.html', context=context)
    else:
        queryset = Authorizations.objects.filter(issuer=request.user.id)
        context = {
            'object_list': queryset
        }
        return render(request=request, template_name='accounts/profile_select_delete.html', context=context)


def select_object_update(request):
    if request.method == 'POST':
        print(request.POST)
        auth_id = request.POST.get('id', False)
        if auth_id:
            return redirect('authorizations:authorization_update', pk=auth_id)
        else:
            queryset = Authorizations.objects.filter(issuer=request.user.id)
            context = {
                'object_list': queryset
            }
            return render(request=request, template_name='accounts/profile_select_update.html.html', context=context)
    else:
        queryset = Authorizations.objects.filter(issuer=request.user.id)
        context = {
            'object_list': queryset
        }
        return render(request=request, template_name='accounts/profile_select_update.html', context=context)


@login_required
def user_page(request):
    queryset = Authorizations.objects.filter(issuer=request.user.id)
    context = {
        "user": request.user,
        "object_list": queryset
    }
    return render(request=request, template_name='accounts/profile.html',
                  context=context)


@login_required
def authorization_chart(request):
    chart_data = (
        Authorizations.objects.filter(issuer__user_id=request.user).annotate(date=TruncDay("start_validity")).values(
            "date").annotate(y=Count("id")).order_by("-date")
    )
    expiration_data = (Authorizations.objects.filter(issuer__user_id=request.user, expiration_time__gte=datetime.
                                                     datetime.now(datetime.timezone.utc),
                                                     start_validity__lte=datetime.datetime.now(datetime.timezone.utc)
                                                     ).count())
    as_json = json.dumps(list(chart_data), cls=DjangoJSONEncoder)
    context = {
        'chart_data': as_json,
        'expiration_data': expiration_data,
    }
    return render(request=request, template_name='accounts/profile_statistics.html', context=context)


@login_required
def settings(request):
    profile = Profile.objects.get(user_id=request.user.pk)
    context = {
        'user': request.user,
        'profile': profile
    }
    return render(request=request, template_name='accounts/profile_settings.html', context=context)
