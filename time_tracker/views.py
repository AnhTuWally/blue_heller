from django.shortcuts import render

# import django time module
from django.utils import timezone
from django.utils.dateparse import parse_datetime

# import HTTPResponse from django.http
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse 

from .models import Project, Task, TaskTimer, ActiveTask
from user.models import User

from datetime import timedelta

# Create your views here.

def index(request):
    project_list = Project.objects.all()

    current_user = User.objects.first()


    context = {'project_list': project_list, 'title': 'Time Tracker - Project List', 
               'current_user': current_user}
    
    return render(request, 'time_tracker/index.html', context) 

def project_detail(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'POST':
            # project_name = data['project_name']

            data = request.POST

            project_id = data.get('project_id', None)


            print(project_id)

            project = Project.objects.get(id=project_id)

            if project is None:
                return ""

            active_tasks = ActiveTask.objects.all()
            task_list = project.task_set.all()

            context = {'project': project, "task_list": task_list, "active_tasks": active_tasks}
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


            return HttpResponse('Success')

    return HttpResponseBadRequest('Invalid method')


def create_user(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'POST':
            data = request.POST

            username = data.get('username', None)

            project, created = User.objects.get_or_create(name=username)
            project.save()

            return HttpResponse(username)

    return HttpResponseBadRequest('Invalid method')



def create_task(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'POST':
            # project_name = data['project_name']

            data = request.POST

            project_id = data.get('project_id', None)
            task_name = data.get('task_name', None)

            print(project_id)
            print(task_name)

            project = Project.objects.get(id=project_id)

            task, created = project.task_set.get_or_create(name=task_name, project=project)

            if created:
                return HttpResponse('Success')
            else:
                return HttpResponse('Task Existed')


            return HttpResponse('Success')

    return HttpResponseBadRequest('Invalid method')

# TODO: rename task timer since we are actually creating active task timer
def create_task_timer(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'POST':
            data = request.POST

            task_id = data.get('task_id', None)
            user_id= data.get('user_id', None)

            user = User.objects.get(id=user_id)

            task = Task.objects.get(id=task_id)

            # task_timer, created = TaskTimer.objects.get_or_create(project=task.project, task=task, user=user)

            active_task, created = ActiveTask.objects.get_or_create(user=user, task=task)
            if created:
                active_task.start_time = timezone.now()
                active_task.save()

            return JsonResponse({'active_task_id': active_task.id})


    return HttpResponseBadRequest('Invalid method')


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

            project_id = data.get('project_id', None) 

            active_tasks = ActiveTask.objects.all()

            task_timers = TaskTimer.objects.filter(project__id=project_id)

            context['active_tasks'] = active_tasks if active_tasks else False
            context['task_timers'] = task_timers if task_timers else False
    
    return render(request, 'time_tracker/timeline.html', context) 