from django.db import models
from common.models import BaseModel
# Create your models here.

class TaskTimer(BaseModel):
    """ The timer created eachtime a user starts a task.

    This is used to track the time spent on each task.

    """

    # The parent project of the task
    project = models.ForeignKey("time_tracker.Project", on_delete=models.CASCADE)

    # The parent task of the task timer
    task = models.ForeignKey("time_tracker.Task", on_delete=models.CASCADE)

    # The user who created the task timer
    # This is used to track the time spent on each task by each user
    user = models.ForeignKey("user.User", on_delete=models.SET_NULL, null=True, blank=True)

    # The name of the task timer
    name = models.CharField(null=True, blank=True, max_length=100)

    # A short note of the task timer
    # People can add a note to the task timer to describe what they did
    # Or what they are going to do
    # TODO:
    ##  [ ] Add the note to the UI/webview
    note = models.CharField(null=True, blank=True, max_length=500)

    # The start time of the task timer
    start_time = models.DateTimeField(null=True, blank=True)
    # The end time of the task timer
    end_time = models.DateTimeField(null=True, blank=True)
    # The duration of the task timer
    duration = models.DurationField(null=True, blank=True)

    class Meta:
        # Order the task timers by start time
        # This is the order when they are queried
        ordering = ['-start_time']


    @property
    def duration_str(self):
        """Get the duration of the task timer as a string in the format "00:00:00

        Returns:
            str: the duration of the task timer as a string in the format "00:00:00
        """

        total_seconds = self.duration.total_seconds()
        # convert total_seconds to hours, minutes, seconds
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        seconds = int(total_seconds % 60)
        # format hours minutes  and seconds to 00:00:00
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"