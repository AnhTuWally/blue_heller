from django.urls import path 

from . import views


app_name = 'todo'
urlpatterns = [
    path(r'todo_detail', views.todo_detail, name='todo_detail'),
    path(r'create_todo', views.create_todo, name='create_todo'),
    path(r'delete_todo', views.delte_todo, name='delete_todo'),
    path(r'update_todo', views.update_todo, name='update_todo'),
    path(r'single_todo', views.single_todo, name='single_todo'),
]