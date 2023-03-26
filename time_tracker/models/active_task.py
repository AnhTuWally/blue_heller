
from django.db import models
from common.models import BaseModel
# Create your models here.

class ActiveTask(BaseModel):
    task_timer = models.ForeignKey("time_tracker.TaskTimer", on_delete=models.CASCADE)
    user = models.ForeignKey("user.User", on_delete=models.CASCADE)

    @property
    def name(self):
        return f"{self.task_timer.project.name} - {self.task_timer.task.name}"
    
    @property
    def task(self):
        return self.task_timer.task

    @property
    def project(self):
        return self.task_timer.task.project
