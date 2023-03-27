
from django.db import models
from common.models import BaseModel
# Create your models here.

class ActiveTask(BaseModel):
    task = models.ForeignKey("time_tracker.Task", on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey("user.User", on_delete=models.SET_NULL, null=True, blank=True)
    start_time = models.DateTimeField(null=True, blank=True)

    @property
    def name(self):
        return f"{self.task.project.name} - {self.task.name}"
    
    @property
    def project(self):
        return self.task.project
