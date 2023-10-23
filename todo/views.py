import datetime

from django.shortcuts import render

# import HTTPResponse from django.http
from django.http import HttpResponse, HttpResponseBadRequest

from .models import Todo, TodoHistory, TodoRepeat

# Import the process_ajax_request function from common.views
from common.views import process_ajax_request

from time_tracker.models import Project, Task

# Create your views here.

import logging
logger = logging.getLogger(__name__)

# Create your views here.


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
    
    # NOTE: this is a very non-dynamic way of sorting -> there must be a different way 
    sorted_todo = sorted(todos, key=lambda x: x.priority, reverse=True)

    # split todo into is_done todo and not is_done todo
    is_done_todos = todos.filter(is_done=True)
    not_done_todos = todos.filter(is_done=False)

    context = {'is_done_todos': is_done_todos, 'not_done_todos': not_done_todos}
    
    return render(request, 'todo/todo_detail.html', context)


def single_todo(request):
    data = process_ajax_request(request)

    todo_id = data.get('todo_id', None)

    todo = Todo.objects.get(id=todo_id)
    
    # Math explain
    # There are 100 pixels and 5 levels of urgency
    # => 20 pixels per level of urgency
    # We also want the indicator to starts from the bottom
    # => 100 - 20*urgency
    top_pos = 100 - 20*todo.urgency

    # Math similar to above but it's 200px and priority ranges from 0 to 100
    left_pos = 2*todo.priority

    context = {'todo': todo, 'top_pos': top_pos, 'left_pos': left_pos}

    return render(request, 'todo/single_todo.html', context)


def weekDayToInt(week_day):
    """Convert the weekday string to an int
    0 represents monday -> 6 represents sunday

    Args:
        week_day (str): the weekday string it should be the
        first 3 letters of the weekday
    
    Returns:
        int: the int representation of the weekday
        If the weekday is not valid, return None
    """
    if len(week_day) < 3:
        return None

    week_day = week_day.lower()
    # NOTE this might fail if the weekday is not 3 letters
    if len(week_day) > 3:
        week_day = week_day[:3]

    if week_day == 'mon':
        return 0
    elif week_day == 'tue':
        return 1
    elif week_day == 'wed':
        return 2
    elif week_day == 'thu':
        return 3
    elif week_day == 'fri':
        return 4
    elif week_day == 'sat':
        return 5
    elif week_day == 'sun':
        return 6
    else:
        return None


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


    # This is a string, so we have to convert it to a bool
    is_todo_repeatable = data.get('is_todo_repeatable', 'false')
    is_todo_repeatable = is_todo_repeatable == 'true'

    todo_repeat_interval = data.get('todo_repeat_interval', None)
    todo_repeat_type = data.get('todo_repeat_type', None)
    # NOTE for list we have to use getlist and a key with [] at the end
    todo_repeat_pattern = data.getlist('todo_repeat_pattern[]', [])

    start_date_timestamp = data.get('start_date_timestamp', None)

    if todo_name is None:
        return HttpResponseBadRequest('Invalid todo name')

    project = None
    if project_id:
        project = Project.objects.get(id=project_id)
    
    task = None
    if task_id:
        task = Task.objects.get(id=task_id)
        if not project:
            project = task.project
    
    todo, todo_created = Todo.objects.get_or_create(name=todo_name,
                                                project=project,
                                                task=task,
                                                priority=priority)
    if not todo_created:
        response = HttpResponseBadRequest('Todo already exists')
        return response

    logger.debug(f"New Todo created: {todo}")
    todo.save()

    logger.debug(f"Todo repeatable: {is_todo_repeatable}")

    if is_todo_repeatable:
        if start_date_timestamp is None:
            logger.error("Start date timestamp must be specified for repeatable todos")
            return HttpResponseBadRequest('Start date timestamp must be specified for repeatable todos')
        
        start_date_datetime = datetime.datetime.fromtimestamp(int(start_date_timestamp))
        start_date = start_date_datetime.date()

        logger.debug("Creating todo repeat {}".format(is_todo_repeatable)) 

        todo_repeat_interval = int(todo_repeat_interval)
        if todo_repeat_type not in ['daily', 'weekly', 'monthly']:
            logger.error(f"Invalid todo repeat type: {todo_repeat_type}")
            return HttpResponseBadRequest('Invalid todo repeat type')
        
        if todo_repeat_type == 'weekly':
            if len(todo_repeat_pattern) == 0:
                # Remove the newly created todo
                todo.delete()
                logger.error(f"Todo pattern must be specified for weekly repeat.")
                return HttpResponseBadRequest('Todo pattern must be specified for weekly repeat.')
            for repeat_day in todo_repeat_pattern:
                if repeat_day not in ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']:
                    return HttpResponseBadRequest('Invalid todo repeat pattern')

            # TODO: this might be better if the thet todo_repeat_pattern is a list of ints 
            # When it was first started as the ajax request, it was a list of strings
            todo_repeat_pattern = [str(weekDayToInt(week_day)) for week_day in todo_repeat_pattern]
            repeat_days = ','.join(todo_repeat_pattern) 
        else:
            repeat_days = None


        todo_repeat, created = TodoRepeat.objects.get_or_create(repeat_type=todo_repeat_type,
                                                                repeat_interval=todo_repeat_interval,
                                                                repeat_days=repeat_days,
                                                                repeat_start_date=start_date,
                                                                todo=todo)

        todo_repeat.save()

        # Update the todo with the todo repeat
        todo.todo_repeat = todo_repeat
        todo.save()

    logger.debug(todo.todo_repeat)
    
    response = HttpResponse('New todo created')
    
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
    
    logger.debug(f"Todo {todo_name} ({todo_id}) deleted")

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

    old_is_done = todo.is_done
    todo.is_done = is_done == 'true'
    new_is_done = todo.is_done
    todo.save()

    todo_history = TodoHistory(todo=todo,
                                 modified_field='is_done',
                                 old_value=old_is_done,
                                 new_value=new_is_done)
    todo_history.save()
    logger.debug(f"Todo {todo} updated")
    logger.debug(f"TodoHistory Created {todo_history}")

    return HttpResponse('Success')