import datetime
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django import forms
from .models import Authorizations


class AuthorizationForm2(forms.ModelForm):
    token = forms.CharField(widget=forms.Textarea)

    helper = FormHelper()
    helper.form_id = 'register-form'
    helper.form_method = 'POST'
    helper.add_input(Submit('submit', 'Submit'))

    class Meta:
        model = Authorizations
        fields = ('token', )


class AuthorizationForm(ModelForm):
    start_validity = forms.DateTimeField(help_text='format: MM/dd/yyyy HH:mm')
    expiration_time = forms.DateTimeField(help_text='format: MM/dd/yyyy HH:mm')

    helper = FormHelper()
    helper.form_id = 'register-form'
    helper.form_method = 'POST'
    helper.add_input(Submit('submit', 'Submit'))

    class Meta:
        model = Authorizations
        fields = ('server', 'client', 'start_validity', 'expiration_time')

    # This is the method to check more field a time.
    # It overrides the clean function so you have to call the parent clean function and
    # fill the cleaned_data attribute
    def clean(self):
        super().clean()
        expiration_time = self.cleaned_data.get('expiration_time')
        start_validity = self.cleaned_data.get('start_validity')
        time_now = datetime.datetime.now(datetime.timezone.utc)
        if start_validity is None:
            start_validity = time_now
        if start_validity and expiration_time and expiration_time <= start_validity:
            raise ValidationError("The expiration time is before the start validity time")
        if expiration_time and expiration_time <= time_now:
            raise ValidationError("The expiration time is before the current time")
        if start_validity and start_validity < time_now:
            raise ValidationError("The start validity time is before the current time")

    # This are the method if you want check a field a time.
    # They are running after the clean function so the data are in the cleaned_data dictionary
#    def clean_start_validity(self):
#        data = self.cleaned_data['start_validity']
#           if data:
#            raise ValidationError("You have forgotten about Fred!")

#    def clean_expiration_time(self):
#        data = self.cleaned_data['expiration_time']
#        if data:
#            raise ValidationError("You have forgotten about Fred!")

