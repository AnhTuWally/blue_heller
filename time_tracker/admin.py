from django.contrib import admin

from .models import Project, Task, TaskTimer, ActiveTask

# Register your models here.
admin.site.register(Project)
admin.site.register(Task)
admin.site.register(TaskTimer)
admin.site.register(ActiveTask)

