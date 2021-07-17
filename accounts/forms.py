from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django import forms
from .models import Profile


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


class EmailChangeForm(forms.Form):
    """
    A form that lets a user change set their email while checking for a change in the 
    e-mail.
    """
    error_messages = {
        'email_mismatch': "The two email addresses fields didn't match.",
        'not_changed': "The email address is the same as the one already defined.",
    }

    new_email1 = forms.EmailField(
        label="New email address",
        widget=forms.EmailInput,
    )

    new_email2 = forms.EmailField(
        label="New email address confirmation",
        widget=forms.EmailInput,
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(EmailChangeForm, self).__init__(*args, **kwargs)

    def clean_new_email1(self):
        old_email = self.user.email
        new_email1 = self.cleaned_data.get('new_email1')
        if new_email1 and old_email:
            if new_email1 == old_email:
                raise forms.ValidationError(
                    self.error_messages['not_changed'],
                    code='not_changed',
                )
        return new_email1

    def clean_new_email2(self):
        new_email1 = self.cleaned_data.get('new_email1')
        new_email2 = self.cleaned_data.get('new_email2')
        if new_email1 and new_email2:
            if new_email1 != new_email2:
                raise forms.ValidationError(
                    self.error_messages['email_mismatch'],
                    code='email_mismatch',
                )
        return new_email2

    def save(self, commit=True):
        email = self.cleaned_data["new_email1"]
        self.user.email = email
        if commit:
            self.user.save()
        return self.user


class PublicKeyChangeForm(forms.Form):

    error_messages = {
        'not_changed': "The public key is the same as the one already defined.",
    }
    new_public_key = forms.CharField(
        label="New public key",
        widget=forms.Textarea,
    )

    def __init__(self, user, *args, **kwargs):
        self.profile = Profile.objects.get(user_id=user.pk)
        super(PublicKeyChangeForm, self).__init__(*args, **kwargs)

    def clean_new_public_key(self):
        profile = self.profile
        old_public_key = profile.public_key
        new_public_key = self.cleaned_data.get('new_public_key')
        if new_public_key and old_public_key:
            if new_public_key == old_public_key:
                raise forms.ValidationError(
                    self.error_messages['not_changed'],
                    code='not_changed',
                )
        return new_public_key

    def save(self, commit=True):
        public_key = self.cleaned_data["new_public_key"]
        self.profile.public_key = public_key
        if commit:
            self.profile.save()
        return self.profile
