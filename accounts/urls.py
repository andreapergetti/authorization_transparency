from django.urls import path, reverse_lazy
from accounts.views import ResetPasswordView, register, userpage, authorization_chart, settings, SelectObjectProfile, \
    select_object, email_change, public_key_change
from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [
    path('user_create', register, name='user-create'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/registration/login.html'), name='login'),
    path('logout', auth_views.LogoutView.as_view(template_name='accounts/registration/logged_out.html'), name='logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='accounts/password_change.html'),
         name='password-change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='accounts/password_change_done.html'), name='password-change-done'),
    path('password_reset/', ResetPasswordView.as_view(), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(success_url=reverse_lazy(
        'accounts:password_reset_complete'), template_name='accounts/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('reset/done', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),
    path('profile/', userpage, name='profile'),
    path('profile/select/', select_object, name='profile-select'),
    path('profile/statistics/', authorization_chart, name='profile-statistics'),
    path('profile/settings/', settings, name='profile-settings'),
    path('profile/settings/email_change/', email_change, name='email-change'),
    path('profile/settings/public_key_change/', public_key_change, name='public-key-change'),
]
