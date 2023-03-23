from django.shortcuts import render

# import django time module
from django.utils import timezone

# import HTTPResponse from django.http
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse 

from .models import Project, Task, TaskTimer
import json

# Create your views here.

def index(request):
    project_list = Project.objects.all()

    context = {'project_list': project_list, 'title': 'Time Tracker - Project List'}
    
    return render(request, 'time_tracker/index.html', context) 

def project_detail(request, project_id):
    project = Project.objects.get(id=project_id)
    task_list = project.task_set.all()

    first_task = task_list.first()
    # get the set of all task_timer for the first task
    task_timer_list = ()

    print(task_timer_list)

    context = {'project': project, "task_list": task_list,'title': 'Time Tracker Project Detail'}
    return render(request, 'time_tracker/project_detail.html', context)

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
                return HttpResponse('Project Existed')


            return HttpResponse('Success')

    return HttpResponseBadRequest('Invalid method')


def create_task_timer(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'POST':
            data = request.POST

            task_id = data.get('task_id', None)

            task = Task.objects.get(id=task_id)

            task_timer = TaskTimer.objects.create(project=task.project, task=task)

            task_timer.start_time = timezone.now()

            task_timer.save()

            return JsonResponse({'task_timer_id': task_timer.id})


    return HttpResponseBadRequest('Invalid method')


def stop_task_timer(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'POST':
            data = request.POST

            task_timer_id = data.get('task_timer_id', None)
            
            if task_timer_id is None:
                return HttpResponseBadRequest('Invalid task timer id')

            task_timer = TaskTimer.objects.get(id=task_timer_id)

            if task_timer.end_time is not None:
                return HttpResponseBadRequest('Task timer already stopped')

            task_timer.end_time = timezone.now()
            task_timer.duration = task_timer.end_time - task_timer.start_time

            task_timer.save()

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
