from django.forms import ModelForm
from .models import Authorizations


class AccountForm(ModelForm):
    class Meta:
        model = Authorizations
        fields = ('email', 'password', 'identifier', 'public_key')
