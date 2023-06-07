from django.urls import path 

from . import views


app_name = 'status'
urlpatterns = [
    path(r'status_detail', views.status_detail, name='status_detail'),
    path(r'create_status', views.create_status, name='create_status'),
    path(r'toggle_status', views.toggle_status, name='toggle_status'),
] 