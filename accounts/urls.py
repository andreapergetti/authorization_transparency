from django.urls import path
from accounts.views import UserCreateView, ResetPasswordView, register, ProfileView, userpage, authorization_chart
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
    path('password_reset/', ResetPasswordView.as_view(), name='password-reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/password_reset_done.html'), name='password-reset-done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView, name='password-reset-confirm'),
    path('reset/done', auth_views.PasswordResetCompleteView, name='password-reset-complete'),
    path('profile/', userpage, name='profile'),
    path('profile/statistics/', authorization_chart, name='profile-statistics'),
]
