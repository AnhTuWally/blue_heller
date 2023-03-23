from django.urls import path 

from . import views

app_name = 'time_tracker'
urlpatterns = [
    path(r'', views.index, name='index'),
    path(r'project_detail/<uuid:project_id>', views.project_detail, name='project_detail'),
    path(r'create_project', views.create_project, name='create_project'),
    path(r'create_task', views.create_task, name='create_task'),
    path(r'create_task_timer', views.create_task_timer, name='create_task_timer'),
    path(r'stop_task_timer', views.stop_task_timer, name='stop_task_timer'),
    path(r'delete_task_timer', views.delete_task_timer, name='delete_task_timer')
]
