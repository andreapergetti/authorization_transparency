from django.urls import path
from . import views

app_name = 'authorizations'

urlpatterns = [
    path('authorization/create', views.AuthorizationCreate.as_view(), name='authorization_create'),
    path('authorization/<int:pk>/detail', views.AuthorizationDetail.as_view(), name='authorization_detail'),
    path('authorization/<int:pk>/delete', views.AuthorizationDelete.as_view(), name='authorization_delete'),
    # path('authorization/list', views.AuthorizationList.as_view(), name='authorization_list'),
]
