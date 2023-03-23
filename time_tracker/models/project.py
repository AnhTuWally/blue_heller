from django.db import models
from .base_model import BaseModel
# Create your models here.

class Project(BaseModel):
    name = models.CharField(null=True, blank=True, max_length=100)
    description = models.CharField(null=True, blank=True, max_length=500)

