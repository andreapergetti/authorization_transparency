from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django import forms


class RegisterForm(UserCreationForm):
    public_key = forms.CharField(required=True, widget=forms.Textarea)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email', 'public_key']
