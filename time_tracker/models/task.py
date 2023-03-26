from django.db import models
from common.models import BaseModel

from datetime import timedelta
# Create your models here.

class Task(BaseModel):
    project = models.ForeignKey("time_tracker.Project", on_delete=models.CASCADE)

    name = models.CharField(null=True, blank=True, max_length=100)
    description = models.CharField(null=True, blank=True, max_length=500)

    @property
    def total_time(self):
        total = timedelta()
        for task_timer in self.tasktimer_set.all():
            if task_timer.duration:
                total +=task_timer.duration
        
        return total

