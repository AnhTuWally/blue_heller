from django.db import models
from .base_model import BaseModel
# Create your models here.

class TaskTimer(BaseModel):
    project = models.ForeignKey("time_tracker.Project", on_delete=models.CASCADE)
    task = models.ForeignKey("time_tracker.Task", on_delete=models.CASCADE)

    name = models.CharField(null=True, blank=True, max_length=100)
    note = models.CharField(null=True, blank=True, max_length=500)

    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)

    class meta:
        ordering = ['-start_time']
    