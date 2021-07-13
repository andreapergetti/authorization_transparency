from django.urls import path
from .views import AuthorizationListAPIView, AuthorizationCreateAPIView, \
    AuthorizationRetrieveUpdateAPIView, AuthorizationRetrieveDestroyAPIView

app_name = 'api'

urlpatterns = [
    path('authorizations', AuthorizationListAPIView.as_view()),
    path('authorizations/create', AuthorizationCreateAPIView.as_view()),
    path('authorizations/<int:pk>/update', AuthorizationRetrieveUpdateAPIView.as_view()),
    path('authorizations/<int:pk>/delete', AuthorizationRetrieveDestroyAPIView.as_view(), name='authorization_delete')
]