from django.shortcuts import render

# import django time module
from django.utils import timezone
from django.utils.dateparse import parse_datetime

# import HTTPResponse from django.http
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse 

from .models import Project, Task, TaskTimer, ActiveTask

from status.models import ProjectStatus, TaskStatus

from user.models import User

from datetime import timedelta

from django.views import View

from todo.models import TodoHistory


# Import the process_ajax_request function from common.views
from common.views import process_ajax_request

# Create your views here.

import logging
logger = logging.getLogger(__name__)

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

def node_editor(requests):
    """ A function to render the node editor page

    Args:
        requests (_type_): _description_

    Returns:
        _type_: _description_
    """
    context = {}
    return render(requests, 'time_tracker/node_editor.html', context)

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

    task_list = []

    show_project_name_on_task = False

    # If there is no project id, return a defult page with no project
    if not project_id:

        show_project_name_on_task = True

        # Query for the last 5 tasks that was tracked
        # end hese task as task_list to the context
        ordered_task_timers = TaskTimer.objects.all().order_by('-end_time')


        # NOTE: this is very inefficient
        # If the number of task timers is large, this will take a long time
        for task_timer in ordered_task_timers:
            if len(task_list) >= 5:
                break

            task = task_timer.task

            if task not in task_list:
                task_list.append(task)
            

        return render(request, 'time_tracker/project_detail.html',
                      {"has_project": False,
                       "task_list": task_list,
                       "show_project_name_on_task": show_project_name_on_task,
                       })

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
                "show_project_name_on_task": show_project_name_on_task,
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


    project, created = Project.objects.get_or_create(name=project_name)
    project.save()

    if created:
        logger.info("New Project Created: {}".format(project_name))
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

    logger.warning("Project Deleted: {}".format(project.name))

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

    logger.debug("Project Status Changed: {} -> {}".format(project.name, status.name))

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
        logger.debug("New Task Created: {}".format(task_name))
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

    logger.warning("Task Deleted: {}".format(task.name))

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

    logger.debug("Task Status Changed: {} -> {}".format(task.name, status.name))

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
        logger.debug("New Active Task Created: {}".format(active_task.name))

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

    end_time = timezone.now()
    duration = end_time - task_timer.start_time

    # If the duration is less than 1 second -> delete
    if duration < timedelta(seconds=1):
        logger.debug(f"Task timer duration is less than 1 second. No Task Timer was created for {active_task}.")
        return HttpResponse(f'Task timer duration is less than 1 second. No new task timer was created for {active_task}.')

    task_timer.end_time = end_time 
    task_timer.duration = duration
    task_timer.save()

    logger.debug(f"ActiveTask {active_task} deleted -> TaskTimer {task_timer} created")

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

    active_task = ActiveTask.objects.get(id=active_task_id)
    active_task.start_time = start_time

    logger.debug("ActiveTask {} start time changed to {}".format(active_task, start_time))

    active_task.save()

    return HttpResponse('Success')


def view_active_task_note(request):
    """View Task timer

    Args:
        request (_type_): _description_

    Returns:
        _type_: _description_
    """

    data = process_ajax_request(request)

    active_task_id = data.get('active_task_id', None)

    active_task = ActiveTask.objects.get(id=active_task_id)

    active_task_note = active_task.note







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

    logger.debug("TaskTimer {} deleted".format(task_timer))

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

    logger.debug("TaskTimer {} edit saved.")

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
    
    # filter the todo histories that have modified_field value of is_done and the new_value to be True
    todo_histories = TodoHistory.objects.filter(modified_field='is_done', new_value=True)
    context['todo_histories'] = todo_histories
    
    return render(request, 'time_tracker/timeline.html', context) 




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

        project_id = None if project_id in ['null', 'undefined'] else project_id

        if project_id:
            tasks = Task.objects.filter(name__icontains=query, project__id=project_id)
        else:
            tasks = Task.objects.filter(name__icontains=query)

        # tasks = Task.objects.all()
        res = [{"value": task.id, "name": "{} - {}".format(task.name, task.project.name)} for task in tasks]

        return JsonResponse(res, safe=False)

