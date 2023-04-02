from django.db import models
from common.models import BaseModel
from django.apps import apps


class MasterStatus(BaseModel):
    name = models.CharField(null=True, blank=True, max_length=100)
    description = models.CharField(null=True, blank=True, max_length=500)
    color = models.CharField(null=True, blank=True, max_length=10)

    project_status = models.ForeignKey('status.ProjectStatus', on_delete=models.SET_NULL, null=True, blank=True)
    task_status = models.ForeignKey('status.TaskStatus', on_delete=models.SET_NULL, null=True, blank=True)
    note_status = models.ForeignKey('status.NoteStatus', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

    def create_project_status(self):
        ProjectStatus = apps.get_model('status', 'ProjectStatus')
        self.project_status = ProjectStatus.objects.create(master_status=self, name=self.name, description=self.description, color=self.color)
        return self.project_status
    
    def create_task_status(self):
        TaskStatus = apps.get_model('status', 'TaskStatus')
        self.task_status = TaskStatus.objects.create(master_status=self, name=self.name, description=self.description, color=self.color)        
        return self.task_status
    
    def create_note_status(self):
        NoteStatus = apps.get_model('status', 'NoteStatus')
        self.note_status = NoteStatus.objects.create(master_status=self, name=self.name, description=self.description, color=self.color)
        return self.note_status
    