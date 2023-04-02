from django.contrib import admin

from .models import ProjectStatus, TaskStatus, NoteStatus

# Register your models here.
admin.site.register(ProjectStatus)
admin.site.register(TaskStatus)
admin.site.register(NoteStatus)