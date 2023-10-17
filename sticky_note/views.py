from django.shortcuts import render

from time_tracker.models import Project
from user.models import User
from .models import StickyNote

from django.http import HttpResponseBadRequest, JsonResponse 

# import process_ajax_request from common.views
from common.views import process_ajax_request

# Create your views here.

def view_notes(request):
    """ Query the database for all notes and return them to the user
    If the project_id is provided, only return notes for that project

    Args:
        request (ajax): The ajax request

    Returns:
        render: The rendered template with the notes
    """

    # Get the data from the request
    try:
        data = process_ajax_request(request)
    except ValueError as e:
        return HttpResponseBadRequest(e)

    # Get the project_id from the data 
    project_id = data.get('project_id', None)
    
    # Get the project if the project_id is provided
    project = Project.objects.get(id=project_id) if project_id else None

    # If the project exists, get all notes for the project
    if project:
        # Get all notes for the project
        notes = StickyNote.objects.filter(project=project)
        has_project = True
    else:
        # Get all notes for all projects
        notes = StickyNote.objects.filter()
        has_project = False

    # Create the context for the template
    context = {'notes': notes, "has_project": has_project}

    return render(request, 'sticky_note/note_view.html', context)


def create_note(request):
    """ A function to create a new note

    Args:
        request (ajax): The ajax post request to create the note

    Returns:
        json: The json response with the note data
    """

    try:
        data = process_ajax_request(request)
    except ValueError as e:
        return HttpResponseBadRequest(e)

    try:
        project_id = data.get('project_id', None)
        note_name = data.get('name', None)
        content = data.get('content', None)
        user_id = data.get('user_id', None)

        project = Project.objects.get(id=project_id)
        user = User.objects.get(id=user_id)

        note = StickyNote.objects.create(project=project, name=note_name, note=content, user=user)

        response_data = {'note_id': note.id, 'note_name': note.name, 'note_content': note.note, 
                         'user_id': note.user.id, 'user_name': note.user.name}
    except Exception as e:
        response_data = {'error': str(e), 'success': False}

    return JsonResponse(response_data)

        
def delete_note(request):
    """ A function to delete a note

    Args:
        request (ajax): The ajax post request to delete the note

    Returns:
        Json: The json response with the note data. success will be True if the note was deleted
    """

    try:
        data = process_ajax_request(request)
    except ValueError as e:
        return HttpResponseBadRequest(e)

    note_id = data.get('note_id', None)

    try:
        note = StickyNote.objects.get(id=note_id)
        note.delete()

        response_data = {'note_id': note_id, 'success': True}
    except StickyNote.DoesNotExist:
        response_data = {'note_id': note_id, 'success': False}
    
    return JsonResponse(response_data)
