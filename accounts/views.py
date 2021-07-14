from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordResetView
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count
from django.db.models.functions import TruncDay
from django.http import JsonResponse
from django.shortcuts import render, redirect
import datetime
import json

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from accounts.forms import RegisterForm
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


class UserCreateView(CreateView):
    form_class = RegisterForm
    template_name = 'accounts/user_create.html'
    success_url = reverse_lazy('homepage')


class ResetPasswordView(PasswordResetView):
    template_name = 'accounts/password_reset.html'
    success_url = reverse_lazy('accounts:password-reset-done')


@login_required
def userpage(request):
    queryset = Authorizations.objects.filter(issuer=request.user.id)
    context = {
        "user": request.user,
        "object_list": queryset
    }
    return render(request=request, template_name='accounts/profile.html',
                  context=context)


class ProfileView(LoginRequiredMixin, ListView):
    model = Authorizations
    template_name = 'accounts/profile.html'
#    return render(request=request)

#    def get_queryset(self):
#        return Profile.objects.filter(user=self.kwargs['pk'])


def authorization_chart(request):
    chart_data = (
        Authorizations.objects.filter(issuer__user_id=request.user).annotate(date=TruncDay("start_validity")).values(
            "date").annotate(y=Count("id")).order_by("-date")
    )
    expiration_data = (Authorizations.objects.filter(issuer__user_id=request.user, expiration_time__gte=datetime.
                                                     datetime.now(datetime.timezone.utc)).count())
    as_json = json.dumps(list(chart_data), cls=DjangoJSONEncoder)
    context={
        'chart_data': as_json,
        'expiration_data': expiration_data,
    }
    return render(request=request, template_name='accounts/profile_statistics.html', context=context)
