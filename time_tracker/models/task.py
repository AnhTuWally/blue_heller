from django.db import models
from .base_model import BaseModel
# Create your models here.

class Task(BaseModel):
    project = models.ForeignKey("time_tracker.Project", on_delete=models.CASCADE)

    name = models.CharField(null=True, blank=True, max_length=100)
    description = models.CharField(null=True, blank=True, max_length=500)

