import uuid

from django.db import models

class BaseModel(models.Model):
    id = models.UUIDField(
        primary_key = True,
        default = uuid.uuid4,
        help_text = "Unique ID for this particular object across whole database",
        unique = True
    )
    time_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    time_modified = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    # TODO: make created by a model
    created_by = models.CharField(null=True, blank=True, max_length=100)

    class Meta:
        abstract = True
