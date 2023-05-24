from django.shortcuts import render

# import django time module
from django.utils import timezone
from django.utils.dateparse import parse_datetime

# import HTTPResponse from django.http
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse 

from .models import Project, Task, TaskTimer, ActiveTask, Todo 

from status.models import ProjectStatus, TaskStatus, NoteStatus

from user.models import User

from datetime import timedelta

from django.views import View

# Create your views here.

def index(request):
    project_list = Project.objects.all()


    context = {'project_list': project_list, 'title': 'Time Tracker - Project List'}
    
    return render(request, 'time_tracker/index.html', context) 

def project_detail(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'POST':
            # project_name = data['project_name']

            data = request.POST

            project_id = data.get('project_id', None)

            if not project_id:
                return render(request, 'time_tracker/project_detail.html', {"has_project": False})

            project_statuses = ProjectStatus.objects.all()
            task_statuses = TaskStatus.objects.all()
            note_statuses = NoteStatus.objects.all()

            project = Project.objects.get(id=project_id)

            if project is None:
                return ""

            active_tasks = ActiveTask.objects.all()
            task_list = project.task_set.all()

            context = {'project': project, "task_list": task_list, "active_tasks": active_tasks,
                       "project_statuses": project_statuses, "task_statuses": task_statuses,
                       "note_statuses": note_statuses, "has_project": True}
            return render(request, 'time_tracker/project_detail.html', context)


def task_detail(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'POST':
            # project_name = data['project_name']

            data = request.POST

            task_id = data.get('task_id', None)

            task = Task.objects.get(id=task_id)

            task_timer_list = task.tasktimer_set.all()

            if not task_timer_list:
                task_timer_list = False

            context = {'task': task, "task_timer_list": task_timer_list}
            return render(request, 'time_tracker/task_detail.html', context)
    
    return HttpResponseBadRequest('Invalid method')

def delete_task(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'POST':
            # project_name = data['project_name']

            data = request.POST

            task_id = data.get('task_id', None)

            task = Task.objects.get(id=task_id)

            task.delete()

            return HttpResponse('Success')
    
    return HttpResponseBadRequest('Invalid method')

def create_project(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'POST':
            # project_name = data['project_name']

            data = request.POST

            project_name = data.get('project_name', None)

            project, created = Project.objects.get_or_create(name=project_name)
            project.save()

            if created:
                return HttpResponse('Success')
            else:
                return HttpResponse('Project Existed')

    return HttpResponseBadRequest('Invalid method')


def create_task(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'POST':
            # project_name = data['project_name']

            data = request.POST

            project_id = data.get('project_id', None)
            task_name = data.get('task_name', None)

            project = Project.objects.get(id=project_id)

            task, created = project.task_set.get_or_create(name=task_name, project=project)

            if created:
                return HttpResponse('Success')
            else:
                return HttpResponse('Task Existed')

    return HttpResponseBadRequest('Invalid method')

# TODO: rename task timer since we are actually creating active task timer
def create_task_timer(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'POST':
            data = request.POST

            task_id = data.get('task_id', None)
            user_id = data.get('user_id', None)

            user = User.objects.get(id=user_id)

            task = Task.objects.get(id=task_id)

            # task_timer, created = TaskTimer.objects.get_or_create(project=task.project, task=task, user=user)

            active_task, created = ActiveTask.objects.get_or_create(user=user, task=task)
            if created:
                active_task.start_time = timezone.now()
                active_task.save()

            return JsonResponse({'active_task_id': active_task.id})


    return HttpResponseBadRequest('Invalid method')


def change_start_time(request):
    data = process_ajax_request(request)

    active_task_id = data.get('active_task_id', None)
    start_time = data.get('start_time', None)

    start_time = parse_datetime(start_time)

    if not start_time:
        return HttpResponseBadRequest('Invalid start time')

    task_timer = ActiveTask.objects.get(id=active_task_id)
    task_timer.start_time = start_time

    task_timer.save()

    return HttpResponse('Success')


def stop_task_timer(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'POST':
            data = request.POST

            active_task_id = data.get('active_task_id', None)
            user_id= data.get('user_id', None)

            print(active_task_id)
            
            if active_task_id is None:
                return HttpResponseBadRequest('Invalid task timer id')

            active_task = ActiveTask.objects.get(id=active_task_id)

            task_timer = TaskTimer(project=active_task.task.project, task=active_task.task, user=active_task.user, start_time=active_task.start_time)
            task_timer.end_time = timezone.now()
            task_timer.duration = task_timer.end_time - task_timer.start_time
            task_timer.save()

            active_task.delete()

            #timedelta of 1 second
            if task_timer.duration < timedelta(seconds=1):
                task_timer.delete()
                return HttpResponse('Task timer duration is less than 1 second. Deleting')

            return HttpResponse('Success')

    return HttpResponseBadRequest('Invalid method')


def delete_task_timer(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'POST':
            data = request.POST

            task_timer_id = data.get('task_timer_id', None)
            
            if task_timer_id is None:
                return HttpResponseBadRequest('Invalid task timer id')

            task_timer = TaskTimer.objects.get(id=task_timer_id)

            task_timer.delete()

            return HttpResponse('Success')

    return HttpResponseBadRequest('Invalid method')

def delete_project(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'POST':
            data = request.POST

            project_id = data.get('project_id', None)
            
            if project_id is None:
                return HttpResponseBadRequest('Invalid project id')

            project = Project.objects.get(id=project_id)

            project.delete()

            return HttpResponse('Success')

    return HttpResponseBadRequest('Invalid method')


def edit_task_timer(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'POST':
            data = request.POST

            task_timer_id = data.get('task_timer_id', None)
            start_time_value = data.get('start_time_value', None)
            end_time_value = data.get('end_time_value', None)
            
            if task_timer_id is None:
                return HttpResponseBadRequest('Invalid task timer id')

            task_timer = TaskTimer.objects.get(id=task_timer_id)

            # GOHERE
            start_time = parse_datetime(start_time_value)
            end_time = parse_datetime(end_time_value)

            task_timer.start_time = start_time
            task_timer.end_time = end_time

            task_timer.duration = end_time - start_time

            task_timer.save()

            return JsonResponse({'task_timer_id': task_timer_id, 
                                'start_time': start_time,
                                'end_time': end_time,
                                'duration': task_timer.duration})
    return HttpResponseBadRequest('Invalid method')


def timeline(request):

    context={}

    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'POST':
            data = request.POST

            active_tasks = ActiveTask.objects.all()
            project_id = data.get('project_id', None) 

            if project_id == 'all':
                task_timers = TaskTimer.objects.all()
            else:
                task_timers = TaskTimer.objects.filter(project__id=project_id)

            context['active_tasks'] = active_tasks if active_tasks else False
            context['task_timers'] = task_timers if task_timers else False
    
    return render(request, 'time_tracker/timeline.html', context) 


def set_project_status(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'POST':
            data = request.POST

            project_id = data.get('project_id', None)
            project_status_id = data.get('project_status_id', None)

            if project_id is None:
                return HttpResponseBadRequest('Invalid project id')

            if project_status_id is None:
                return HttpResponseBadRequest('Invalid project status id')

            project = Project.objects.get(id=project_id)

            status = ProjectStatus.objects.get(id=project_status_id)


            project.status = status
            project.save()

            return HttpResponse('Success')

    return HttpResponseBadRequest('Invalid method')


def set_task_status(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'POST':
            data = request.POST

            task_id = data.get('task_id', None)
            task_status_id = data.get('task_status_id', None)

            if task_id is None:
                return HttpResponseBadRequest('Invalid task id')


            if task_status_id is None:
                return HttpResponseBadRequest('Invalid task status id')

            task = Task.objects.get(id=task_id)
            status = TaskStatus.objects.get(id=task_status_id)

            task.status = status
            task.save()

            return HttpResponse('Success')

    return HttpResponseBadRequest('Invalid method')


def process_ajax_request(request, method='POST'):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == method:
            data = request.POST
            return data

    return HttpResponseBadRequest('Invalid method')

def todo_detail(request):
    data = process_ajax_request(request)

    project_id = data.get('project_id', None)

    if not project_id:
        todos = Todo.objects.all()
        tasks = Task.objects.all()
    else:
        todos = Todo.objects.filter(project__id=project_id)

    context = {'todos': todos}
    
    return render(request, 'time_tracker/todo_detail.html', context)


def create_todo(request):
    data = process_ajax_request(request)

    todo_name = data.get('todo_name', None)
    task_id = data.get('task_id', None)
    project_id = data.get('project_id', None)
    priority = data.get('priority', 0)

    if todo_name is None:
        return HttpResponseBadRequest('Invalid todo name')

    if project_id:
        project = Project.objects.get(id=project_id)
    else:
        project = None
    
    if task_id:
        task = Task.objects.get(id=task_id)
    else:
        task = None
    
    if project and task:
        todo, created = Todo.objects.get_or_create(name=todo_name, project=project, task=task)
    
    elif project:
        todo, created = Todo.objects.get_or_create(name=todo_name, project=project)

    elif task:
        todo, created = Todo.objects.get_or_create(name=todo_name, task=task, project=task.project)
    
    else:
        todo, created = Todo.objects.get_or_create(name=todo_name, task=None, project=None)
        print('created: ', created)


    if created:
        response = HttpResponse('Success')
        todo.priority = priority
    else:
        response = HttpResponse('Todo Existed. PLease check again. Priority unchanged.')

    todo.save()

    return response

    

def delte_todo(request):
    data = process_ajax_request(request)

    todo_id = data.get('todo_id', None)

    todo = Todo.objects.get(id=todo_id)

    todo_name = todo.name
    todo_id = todo.id

    todo.delete()

    return HttpResponse('TODO: {} ({}) deleted'.format(todo_name, todo_id))


def update_todo(request):
    data = process_ajax_request(request)

    todo_id = data.get('todo_id', None)
    is_done = data.get('is_done', None)

    todo = Todo.objects.get(id=todo_id)

    todo.is_done = is_done == 'true'

    todo.save()

    return HttpResponse('Success')


def list_tasks(request):
    data = process_ajax_request(request)

    project_id = data.get('project_id', None)

    if project_id:
        tasks = Task.objects.filter(project__id=project_id)
    else:
        tasks = Task.objects.all()

    task_list = []
    for task in tasks:
        task_list.append({'id': task.id, 'name': task.name})

    print(task_list)
    
    return JsonResponse({'tasks': task_list})

# https://stackoverflow.com/questions/32465052/using-typeahead-js-in-django-project
class TaskView(View):
    def get(self, request):
        query = request.GET.get('query', '')
        project_id = request.GET.get('project_id', None)

        project_id = None if project_id == 'null' else project_id

        if project_id:
            tasks = Task.objects.filter(name__icontains=query, project__id=project_id)
        else:
            tasks = Task.objects.filter(name__icontains=query)

        # tasks = Task.objects.all()
        res = [{"value": task.id, "name": "{} - {}".format(task.name, task.project.name)} for task in tasks]
        return JsonResponse(res, safe=False)