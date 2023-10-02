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


# Import the process_ajax_request function from common.views
from common.views import process_ajax_request

# Create your views here.

def index(request):
    """
    This is the function that renders the index page of the time tracker app
    """
    project_list = Project.objects.all()

    active_tasks = ActiveTask.objects.all()

    # project_list: the list of available projects
    # title: A custom title for the page : TODO - change this to a more meaningful title
    # active_tasks: the list of taks that is currently active/tracking

    context = {'project_list': project_list, 
               'title': 'CODE ME',
               'active_tasks': active_tasks}
    
    return render(request, 'time_tracker/index.html', context) 


# PROJECT
def project_detail(request):
    """ Query the database for a project object with the given project id
    return the project detail page with the project object

    Args:
        request (ajax request): the request object from the ajax call
        the object should contain the project_id of the project that we want to get the details of

    Returns:
        html template: the html template that contains the project details 
    """
    data = process_ajax_request(request)

    project_id = data.get('project_id', None)

    # If there is no project id, return a defult page with no project
    if not project_id:
        return render(request, 'time_tracker/project_detail.html', {"has_project": False})

    # If there is a project id, get the project object  
    project = Project.objects.get(id=project_id)

    # Unable to find the project with the given id -> raise an error
    if project is None:
        raise ValueError("Invalid project id")

    # TODO: do we need to query for these everytime?
    project_statuses = ProjectStatus.objects.all()
    task_statuses = TaskStatus.objects.all()

    task_list = project.task_set.all()

    context = {'project': project, "task_list": task_list, 
                "project_statuses": project_statuses,
                "task_statuses": task_statuses,
                "has_project": True}
    
    # Finally, render the project detail page with the project object
    return render(request, 'time_tracker/project_detail.html', context)


def create_project(request):
    """ Create a project with the given project name

    Args:
        request (_type_): _description_

    Returns:
        HttpResponse: the response either Success or Project Existed
    """
    data = process_ajax_request(request)
    project_name = data.get('project_name', None)

    print("Creating project with name: {}".format(project_name))

    project, created = Project.objects.get_or_create(name=project_name)
    project.save()

    if created:
        return HttpResponse('New Project: "{}" Created.'.format(project_name))
    else:
        return HttpResponse('{} Existed.'.format(project_name))


def delete_project(request):
    """ Delete a project given its project_id

    Args:
        request (_type_): _description_

    Returns:
        _type_: _description_
    """
    data = process_ajax_request(request)
    project_id = data.get('project_id', None)
    
    if project_id is None:
        return HttpResponseBadRequest('Invalid project id')

    project = Project.objects.get(id=project_id)

    project.delete()

    return HttpResponse('Success')


def set_project_status(request):
    """ Set the status of a project

    Args:
        request (_type_): _description_

    Returns:
        _type_: _description_
    """
    data = process_ajax_request(request)

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


# TASK
def task_detail(request):
    """ Query the database for a task object with the given task id
    return the task detail page with the task object

    Args:
        request (requests): the request object from the ajax call

    Returns:
        _type_: _description_
    """

    data = process_ajax_request(request)

    task_id = data.get('task_id', None)

    task = Task.objects.get(id=task_id)

    task_timer_list = task.tasktimer_set.all()

    context = {'task': task, "task_timer_list": task_timer_list}
    return render(request, 'time_tracker/task_detail.html', context)
    

def create_task(request):
    """Create a task object with the given task name

    Args:
        request (_type_): _description_

    Returns:
        HttpResponse: the response either Success or Task Existed
    """
    data = process_ajax_request(request)

    project_id = data.get('project_id', None)
    task_name = data.get('task_name', None)

    project = Project.objects.get(id=project_id)

    task, created = project.task_set.get_or_create(name=task_name, project=project)

    if created:
        return HttpResponse('Success')
    else:
        return HttpResponse('Task Existed')
    

def delete_task(request):
    """ Delete a task object with the given task id

    Args:
        request (ajax request): the request object from the ajax call

    Returns:
        _type_: _description_
    """

    data = process_ajax_request(request)

    task_id = data.get('task_id', None)

    task = Task.objects.get(id=task_id)

    task.delete()

    return HttpResponse('Success')


def set_task_status(request):
    """ Set the status of a task give its task_id and task_status_id

    Args:
        request (_type_): _description_

    Returns:
        _type_: _description_
    """
    data = process_ajax_request(request)

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


def list_tasks(request):
    """List the available tasks given the project_id

    Args:
        request (_type_): _description_

    Returns:
        _type_: _description_
    """
    data = process_ajax_request(request)

    project_id = data.get('project_id', None)

    if project_id:
        tasks = Task.objects.filter(project__id=project_id)
    else:
        tasks = Task.objects.all()

    task_list = []
    for task in tasks:
        task_list.append({'id': task.id, 'name': task.name})

    return JsonResponse({'tasks': task_list})


def load_active_tasks(request):
    """ Query to get the active task

    Args:
        request (_type_): _description_

    Returns:
        _type_: _description_
    """
    active_tasks = ActiveTask.objects.all()

    context = {'active_tasks': active_tasks}
    
    return render(request, 'time_tracker/active_task_detail.html', context) 


# ACTIVE TASK 
def create_active_task(request):
    """ Create an active task to track a task

    Args:
        request (_type_): _description_

    Returns:
        _type_: _description_
    """
    data = process_ajax_request(request)

    task_id = data.get('task_id', None)
    user_id = data.get('user_id', None)

    user = User.objects.get(id=user_id)
    task = Task.objects.get(id=task_id)

    active_task, created = ActiveTask.objects.get_or_create(user=user, task=task)
    if created:
        active_task.start_time = timezone.now()
        active_task.save()

    return JsonResponse({'active_task_id': active_task.id})


def stop_active_task(request):
    """ Stop the currently active task given its active_task_id

    When the active task is stopped

    A TaskTimer object is created to store the infomation on the duration

    Args:
        request (_type_): _description_

    Returns:
        _type_: _description_
    """

    data = process_ajax_request(request)

    active_task_id = data.get('active_task_id', None)
            
    if active_task_id is None:
        return HttpResponseBadRequest('Invalid task timer id')

    active_task = ActiveTask.objects.get(id=active_task_id)

    task_timer = TaskTimer(project=active_task.task.project,
                            task=active_task.task,
                            user=active_task.user,
                            start_time=active_task.start_time)

    # The active task data has been stored in the task timer
    # -> Delete ActiveTask from the db
    active_task.delete()

    task_timer.end_time = timezone.now()
    task_timer.duration = task_timer.end_time - task_timer.start_time
    task_timer.save()


    # If the duration is less than 1 second -> delete
    if task_timer.duration < timedelta(seconds=1):
        task_timer.delete()
        return HttpResponse('Task timer duration is less than 1 second. Deleting')

    return HttpResponse('Success')


def change_start_time(request):
    """Change the start time of an active task given active_task_id and start_time

    Args:
        request (_type_): _description_

    Returns:
        _type_: _description_
    """
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


# TASK TIMER
def delete_task_timer(request):
    """Delete the task timer with the given task timer id

    Args:
        request (_type_): _description_

    Returns:
        HttpResponse: _description_
    """
    data = process_ajax_request(request)

    task_timer_id = data.get('task_timer_id', None)
    
    if task_timer_id is None:
        return HttpResponseBadRequest('Invalid task timer id')

    task_timer = TaskTimer.objects.get(id=task_timer_id)

    task_timer.delete()

    return HttpResponse('Success')


def edit_task_timer(request):
    """Edit the task timer given
    - task_timer_id
    - start_time_value
    - end_time_value

    Args:
        request (_type_): _description_

    Returns:
        JsonResponse: a dictionary that contains:
            - task_timer_id:
            - start_time
            - end_time
            - duration
    """
    data = process_ajax_request(request)

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


def timeline(request):
    """Render the time line bar

    Args:
        request (_type_): _description_

    Returns:
        _type_: _description_
    """
    # Context dictionary to pass to the timeline.html for render
    context = {}

    # Get all the active tasks
    active_tasks = ActiveTask.objects.all()
    context['active_tasks'] = active_tasks if active_tasks else False

    # Get the project_id from he ajax request
    data = process_ajax_request(request)
    project_id = data.get('project_id', None) 

    # If the project_id is all -> show all task timer
    # Else, only show the one from the given project with the id
    if project_id == 'all':
        task_timers = TaskTimer.objects.all()
    else:
        task_timers = TaskTimer.objects.filter(project__id=project_id)

    context['task_timers'] = task_timers if task_timers else False
    
    return render(request, 'time_tracker/timeline.html', context) 


# TODO
def todo_detail(request):
    """ Render the todo view given a project_id
    if the project id is not give, get all the notes

    Args:
        request (_type_): _description_

    Returns:
        _type_: _description_
    """
    data = process_ajax_request(request)

    project_id = data.get('project_id', None)

    if not project_id:
        todos = Todo.objects.all()
    else:
        todos = Todo.objects.filter(project__id=project_id)

    context = {'todos': todos}
    
    return render(request, 'time_tracker/todo_detail.html', context)


def create_todo(request):
    """Create the todo given 
    - todo_name
    - task_id
    - project_id
    - priority

    Args:
        request (_type_): _description_

    Returns:
        _type_: _description_
    """
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
        todo, created = Todo.objects.get_or_create(name=todo_name,
                                                   project=project,
                                                   task=task)
    
    elif project:
        todo, created = Todo.objects.get_or_create(name=todo_name,
                                                   project=project)

    elif task:
        todo, created = Todo.objects.get_or_create(name=todo_name,
                                                   task=task,
                                                   project=task.project)
    
    else:
        todo, created = Todo.objects.get_or_create(name=todo_name,
                                                   task=None,
                                                   project=None)

    if created:
        response = HttpResponse('Success')
        todo.priority = priority
    else:
        response = HttpResponse('Todo Existed. PLease check again. Priority unchanged.')

    todo.save()
    return response


def delte_todo(request):
    """Delete a todo given the todo_id

    Args:
        request (_type_): _description_

    Returns:
        _type_: _description_
    """
    data = process_ajax_request(request)

    todo_id = data.get('todo_id', None)

    todo = Todo.objects.get(id=todo_id)

    todo_name = todo.name
    todo_id = todo.id

    todo.delete()

    return HttpResponse('TODO: {} ({}) deleted'.format(todo_name, todo_id))


def update_todo(request):
    """update the todo given the todo_id and is_done

    this is to update the db of whether the todo is done or not

    Args:
        request (_type_): _description_

    Returns:
        _type_: _description_
    """
    data = process_ajax_request(request)

    todo_id = data.get('todo_id', None)
    is_done = data.get('is_done', None)

    todo = Todo.objects.get(id=todo_id)

    todo.is_done = is_done == 'true'

    todo.save()

    return HttpResponse('Success')


# https://stackoverflow.com/questions/32465052/using-typeahead-js-in-django-project
class TaskView(View):
    def get(self, request):
        """ A function to help with the typeadead view in js

        Args:
            request (_type_): _description_

        Returns:
            _type_: _description_
        """
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

