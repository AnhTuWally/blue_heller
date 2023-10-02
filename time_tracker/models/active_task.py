
from django.db import models
from common.models import BaseModel

class ActiveTask(BaseModel):
    """ The active task is the task that the user is currently working on.

    Once the user starts a task, the active task is created.
    When the user stops the task, the active task is deleted and a task timer is created.


    """
    # The task that the user is currently working on
    task = models.ForeignKey("time_tracker.Task", on_delete=models.CASCADE, null=True, blank=True)
    # The user who created the active task
    user = models.ForeignKey("user.User", on_delete=models.SET_NULL, null=True, blank=True)
    # The start time of the active task
    start_time = models.DateTimeField(null=True, blank=True)

    @property
    def name(self):
        """ Get the name of the active task.
        The name of the active task is a combination of the project name and the task name

        Example: "Project 1 - Task 1"

        Returns:
            str: the name of the active task
        """
        return f"{self.task.project.name} - {self.task.name}"
    
    @property
    def project(self):
        """ The parent project of the active task

        Returns:
            str: the name of the parent project of the active task
        """

        return self.task.project
