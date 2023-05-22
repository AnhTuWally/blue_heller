from django.shortcuts import render

from time_tracker.models import Project
from user.models import User
from .models import StickyNote

from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse 

# Create your views here.

def view_notes(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'POST':
            data = request.POST

            project_id = data.get('project_id', None)

            if not project_id:
                return render(request, 'sticky_note/note_view.html', {"has_project": False})

            project = Project.objects.get(id=project_id)

            if project is None:
                return ""

            notes = StickyNote.objects.filter(project=project)

            context = {'notes': notes, "has_project": True}
            return render(request, 'sticky_note/note_view.html', context)
        


def create_note(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'POST':
            data = request.POST

            project_id = data.get('project_id', None)
            note_name = data.get('name', None)
            content = data.get('content', None)
            user_id = data.get('user_id', None)

            project = Project.objects.get(id=project_id)
            user = User.objects.get(id=user_id)


            note = StickyNote.objects.create(project=project, name=note_name, note=content, user=user)

            return HttpResponse('Success')

        
def delete_note(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'POST':
            data = request.POST

            note_id = data.get('note_id', None)

            print('-'*100)
            print(note_id)
            print('-'*100)

            note = StickyNote.objects.get(id=note_id)

            note.delete()

            return HttpResponse('Success')

        







