from django.db import models
from common.models import BaseModel
# Create your models here.

class Project(BaseModel):
    name = models.CharField(null=True, blank=True, max_length=100)
    description = models.CharField(null=True, blank=True, max_length=500)
    status = models.ForeignKey('status.ProjectStatus', on_delete=models.SET_NULL, null=True, blank=True)



