from django.db import models
from common.models import BaseModel

from datetime import timedelta
# Create your models here.

class Task(BaseModel):
    """A Task  is a unit of work that is part of a project.

    It kept the time spent on task. 
    """

    # The parent project of the task
    project = models.ForeignKey("time_tracker.Project", on_delete=models.CASCADE)

    # The name of the task
    name = models.CharField(null=True, blank=True, max_length=100)

    # A short description of the task
    ## TODO: Need to add the description to the UI/webview
    description = models.CharField(null=True, blank=True, max_length=500)

    # The status of the task
    status = models.ForeignKey('status.TaskStatus', on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def total_time(self):
        """Return the total time spent on the task.

        Returns:
            timedelta: the total time spent on each task
        """
        total = timedelta()

        # Iterate through each task timer and add the duration to the total 
        ## TODO: this might need to be optimized/multi-threaded
        for task_timer in self.tasktimer_set.all():
            if task_timer.duration:
                total +=task_timer.duration
            
        return total
    
    @property
    def total_time_str(self):
        """Return the total time spent on the task as a string in the format "00:00:00

        Returns:
            str: the total time spent on each task as a string in the format "00:00:00
        """
        # get total seconds 
        total_seconds = self.total_time.total_seconds()
        # convert total_seconds to hours, minutes, seconds
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        seconds = int(total_seconds % 60)
        # format hours minutes and seconds to 00:00:00
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

