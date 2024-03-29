from django.urls import path 

from . import views


app_name = 'time_tracker'
urlpatterns = [
    path(r'', views.index, name='index'),
    path(r'project_detail', views.project_detail, name='project_detail'),
    path(r'task_detail', views.task_detail, name='task_detail'),
    path(r'create_project', views.create_project, name='create_project'),
    path(r'delete_project', views.delete_project, name='delete_project'),
    path(r'create_task', views.create_task, name='create_task'),
    path(r'delete_task', views.delete_task, name='delete_task'),
    path(r'create_active_task', views.create_active_task, name='create_active_task'),
    path(r'stop_active_task', views.stop_active_task, name='stop_active_task'),
    path(r'delete_task_timer', views.delete_task_timer, name='delete_task_timer'),
    path(r'edit_task_timer', views.edit_task_timer, name='edit_task_timer'),
    path(r'timeline', views.timeline, name='timeline'),
    path(r'set_project_status', views.set_project_status, name='set_project_status'),
    path(r'set_task_status', views.set_task_status, name='set_task_status'),
    path(r'list_tasks', views.TaskView.as_view(), name='list_tasks'),
    path(r'change_start_time', views.change_start_time, name='change_start_time'),
    path(r'load_active_tasks', views.load_active_tasks, name='load_active_tasks'),
    path(r'view_active_task_note', views.view_active_task_note, name='view_active_task_note'),
    path(r'node_editor', views.node_editor, name='node_editor'),
]
