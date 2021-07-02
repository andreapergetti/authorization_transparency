from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView


class Homepage(TemplateView):
    template_name = 'homepage.html'
