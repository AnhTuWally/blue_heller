from django.db import models
from common.models import BaseModel

class Project(BaseModel):
    """A Project is the biggest unit of work in the time tracker.

    It is made up of tasks.

    """
    name = models.CharField(null=True, blank=True, max_length=100)
    # A short description of the project
    ## TODO:
    ### [ ] Add the description to the UI/webview
    description = models.CharField(null=True, blank=True, max_length=500)
    status = models.ForeignKey('status.ProjectStatus', on_delete=models.SET_NULL, null=True, blank=True)



