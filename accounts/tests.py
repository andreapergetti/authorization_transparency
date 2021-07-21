from django.contrib.auth.models import User
from django.test import TestCase, Client
from authorizations.models import Authorizations


# Create your tests here.
class ProfileViewTest(TestCase):
    def setUp(self):
        self.credentials = {'username': 'test', 'password': 'testing'}
        self.user = User.objects.create_user(**self.credentials)
        # Profile.objects.create(user_id=user.pk)
        self.client.login(username='test', password='testing')

    def test_profile_page_view_with_user_logged(self):
        """
        Check if the username and the queryset correspond to the logged in user
        """
        response = self.client.get('/accounts/profile/')
        print(response.context['user'])
        print(response.context['object_list'])
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['user'].username, 'test')
        self.assertQuerysetEqual(response.context['object_list'],
                                 Authorizations.objects.filter(issuer_id=self.user.pk))

    def test_profile_page_view_with_no_authorizations(self):
        """
        No authorizations --> "No authorization released"
        message should be displayed.
        """
        response = self.client.get('/accounts/profile/')
        #print(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No authorization released")
        self.assertQuerysetEqual(response.context['object_list'], [])

    def test_profile_page_view_with_three_authorizations(self):
        """
        Three authorizations --> The length of object_list must be three
        """
        new_auth1 = {'issuer_id': f'{self.user.pk}', 'server': 's', 'client': 'c',
                     'start_validity': '2021-08-01', 'expiration_time': '2021-08-15'}
        new_auth2 = {'issuer_id': f'{self.user.pk}', 'server': 's2', 'client': 'c2',
                     'start_validity': '2021-08-01', 'expiration_time': '2021-08-15'}
        new_auth3 = {'issuer_id': f'{self.user.pk}', 'server': 's3', 'client': 'c3',
                     'start_validity': '2021-08-01', 'expiration_time': '2021-08-15'}
        Authorizations.objects.create(**new_auth1)
        Authorizations.objects.create(**new_auth2)
        Authorizations.objects.create(**new_auth3)
        response = self.client.get('/accounts/profile/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['object_list']), 3)

    def test_profile_page_view_link(self):
        """
        Check if the link in the profile page return status code 200
        """
        response = self.client.get('/accounts/profile/statistics/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/accounts/profile/settings/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/authorizations/authorization/create')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/accounts/profile/select/')
        self.assertEqual(response.status_code, 200)

    def test_profile_page_view_with_no_user_logged(self):
        """
        No user --> Status code must be unauthorized
        """
        self.client.logout()
        response = self.client.get('/accounts/profile/')
        self.assertRedirects(response, '/accounts/login/?next=/accounts/profile/',
                             status_code=302, target_status_code=200)


