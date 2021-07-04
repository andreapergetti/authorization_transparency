from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django import forms


class RegisterForm(UserCreationForm):
    public_key = forms.CharField(required=True, widget=forms.Textarea)

    helper = FormHelper()
    helper.form_id = 'register-form'
    helper.form_method = 'POST'
    helper.add_input(Submit('submit', 'Submit'))

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email', 'public_key']

#    def clean_public_key(self):
#        public_key = self.cleaned_data['public_key']
#        if public_key.startswith('ssh-rsa') or public_key.startswith('ecdsa-sha2-nistp256') or \
#                public_key.startswith('ecdsa-sha2-nistp384') or public_key.startswith('ecdsa-sha2-nistp521') or \
#                public_key.startswith('ssh-ed255') or
