from django.db import models
from common.models import BaseModel

# Create your models here.
class User(BaseModel):
    name = models.CharField(null=True, blank=True, max_length=100)

    def __str__(self):
        return self.name
