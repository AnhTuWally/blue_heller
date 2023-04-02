from django.db import models
from common.models import BaseModel

# Create your models here.

class Status(BaseModel):
    name = models.CharField(null=True, blank=True, max_length=100)
    description = models.CharField(null=True, blank=True, max_length=500)
    color = models.CharField(null=True, blank=True, max_length=10)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Statuses'
        abstract=True