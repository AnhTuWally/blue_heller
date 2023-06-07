from django.shortcuts import render

# import HTTPResponse from django.http
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse 

from .models import MasterStatus

from common.views import process_ajax_request


def index(request):
    # TODO: implement this page
    return HttpResponse("Hello, world. You're at the status index.")

def create_status(request):
    try:
        data = process_ajax_request(request)
    except ValueError as e:
        return HttpResponseBadRequest(e)
    
    try:
        status_name = data.get('status_name', None)

        # TODO: status_description is not being used
        status_description = data.get('status_description', None)

        project_status = data.get('project_status', None)
        task_status = data.get('task_status', None)
        note_stauts = data.get('note_status', None)

        status, created = MasterStatus.objects.get_or_create(name=status_name)

        # Initialize the status objects
        if project_status == 'true':
            Project_status_obj = status.create_project_status()

        if task_status == 'true':
            task_status_obj = status.create_task_status()
        
        if note_stauts == 'true':
            note_status_obj = status.create_note_status()
        
        status.save()
        json_response = {'status_id': status.id, 'success': True,
                         'project_status': project_status, 'task_status': task_status, 
                         'note_status': note_stauts}
    
    except Exception as e:
        json_response = {'error': str(e), 'success': False}
        

    return JsonResponse(json_response)


def toggle_status(request):
    """Toggle the status of a status object

    Args:
        request (ajax): ajax request

    Returns:
        _type_: _description_
    """
    try:
        data = process_ajax_request(request)
    except ValueError as e:
        return HttpResponseBadRequest(e)

    try:
        status_id = data.get('status_id', None)
        status_type = data.get('status_type', None)
        status = MasterStatus.objects.get(id=status_id)


        project_status_enabled = True if status.project_status else False
        task_status_enabled = True if status.task_status else False
        note_status_enabled = True if status.note_status else False

        # state = {'project_status': project_status_enabled,
                #  'task_status': task_status_enabled,
                #  'note_status': note_status_enabled}

        if status_type == 'project_status':
            status_enabled = project_status_enabled
            if project_status_enabled:
                status.project_status.delete()
            else:
                status.create_project_status()
                status.save()
        
        elif status_type == 'task_status':
            status_enabled = task_status_enabled
            if task_status_enabled:
                status.task_status.delete()
            else:
                status.create_task_status()
                status.save()

        elif status_type == 'note_status':
            status_enabled = note_status_enabled
            if note_status_enabled:
                status.note_status.delete()
            else:
                status.create_note_status()
                status.save()

        else:
            json_response = {'error': 'Invalid status type', 'success': False}
            return JsonResponse(json_response)

        new_status = not status_enabled
        json_response = {'status_id': status.id, 'success': True,
                         'status_enabled': new_status, 'status_type': status_type} 

    except Exception as e:
        json_response = {'error': str(e), 'success': False}

    return JsonResponse(json_response)


def status_detail(request):
    """ returns the status detail page

    Args:
        request (ajax): ajax request

    Returns:
        render: renders the status detail page
    """

    try:
        data = process_ajax_request(request)
    except ValueError as e:
        return HttpResponseBadRequest(e)
    
    try:
        status_id = data.get('status_id', None)
        
        statuses = MasterStatus.objects.all()

        context = {'master_statuses': statuses}

        return render(request, 'status/list_statuses.html', context)
    except Exception as e:
        return HttpResponseBadRequest(e)

