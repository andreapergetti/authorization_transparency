from django.test import TestCase
from .models import Authorizations
from accounts.models import User
from django.core.exceptions import ValidationError
from .forms import AuthorizationForm


# Create your tests here.
class AuthorizationCreateTest(TestCase):
    def setUp(self):
        self.credentials = {'username': 'test', 'password': 'testing'}
        self.user = User.objects.create_user(**self.credentials)
        # Profile.objects.create(user_id=user.pk)
        self.client.login(username='test', password='testing')

    def test_have_expiration_date_before_start_validity(self):
        self.client.get('/authorizations/authorization/create')
        form_data = {'server': 's', 'client': 'c',
                     'start_validity': '2021-08-15', 'expiration_time': '2021-08-01'}
        form = AuthorizationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['__all__'][0], 'The expiration time is before the start validity time')

    def test_have_start_validity_before_now(self):
        form_data = {'server': 's', 'client': 'c',
                     'start_validity': '2021-07-10', 'expiration_time': '2021-08-01'}
        form = AuthorizationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['__all__'][0], 'The start validity time is before the current time')

    def test_have_expiration_time_before_now(self):
        form_data = {'server': 's', 'client': 'c',
                     'start_validity': '2021-07-01', 'expiration_time': '2021-07-02'}
        form = AuthorizationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['__all__'][0], 'The expiration time is before the current time')

    def test_without_field(self):
        form_data = {'server': 's', 'client': 'c', 'expiration_time': '2021-08-15'}
        form = AuthorizationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['start_validity'][0], 'This field is required.')
        form_data = {'client': 'c', 'start_validity': '2021-07-01',
                     'expiration_time': '2021-07-02'}
        form = AuthorizationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['server'][0], 'This field is required.')
        form_data = {'server': 's', 'start_validity': '2021-07-01',
                     'expiration_time': '2021-07-02'}
        form = AuthorizationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['client'][0], 'This field is required.')
        form_data = {'server': 's', 'client': 'c',
                     'start_validity': '2021-07-01'}
        form = AuthorizationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['expiration_time'][0], 'This field is required.')

