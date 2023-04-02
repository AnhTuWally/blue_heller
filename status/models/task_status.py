from django.db import models
from .status import Status

class TaskStatus(Status):

    master_status = models.ForeignKey('status.MasterStatus', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name