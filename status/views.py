from django.shortcuts import render

# import HTTPResponse from django.http
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse 

from .models import MasterStatus


def index(request):

    return HttpResponse("Hello, world. You're at the status index.")

def create_stauts(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'POST':
            data = request.POST

            status_name = data.get('status_name', None)
            status_description = data.get('status_description', None)
            project_status = data.get('project_status', None)
            task_status = data.get('task_status', None)
            note_stauts = data.get('note_status', None)

            # TODDO: need to handle description
            status, created = MasterStatus.objects.get_or_create(name=status_name)

            if project_status == 'true':
                Project_status_obj = status.create_project_status()

            if task_status == 'true':
                task_status_obj = status.create_task_status()
            
            if note_stauts == 'true':
                note_status_obj = status.create_note_status()
            
            status.save()

            return JsonResponse({'status_id': status.id})

    return HttpResponseBadRequest('Invalid method')


def toggle_status(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'POST':
            data = request.POST


            status_id = data.get('status_id', None)

            status_type = data.get('status_type', None)

            
            status = MasterStatus.objects.get(id=status_id)

            if status_type == 'project_status':
                if status.project_status:
                    status.project_status.delete()
                else:
                    status.create_project_status()
                    status.save()
            
            if status_type == 'task_status':
                if status.task_status:
                    status.task_status.delete()
                else:
                    status.create_task_status()
                    status.save()

            if status_type == 'note_status':
                if status.note_status:
                    status.note_status.delete()
                else:
                    status.create_note_status()
                    status.save()


            return HttpResponse('Status Modified')

    return HttpResponseBadRequest('Invalid method')

def status_detail(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'POST':
            data = request.POST

            status_id = data.get('status_id', None)
            
            statuses = MasterStatus.objects.all()

            context = {'master_statuses': statuses}

            return render(request, 'status/list_statuses.html', context)


    return HttpResponseBadRequest('Invalid method')
