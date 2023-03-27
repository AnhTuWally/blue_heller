from django.urls import path 
from .import views

app_name = 'sticky_note'

urlpatterns = [
    path(r'view_notes', views.view_notes, name='view_notes'),
    path(r'create_note', views.create_note, name='create_note'),
    path(r'delete_note', views.delete_note, name='delete_note'),
]