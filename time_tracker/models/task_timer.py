from django.db import models
from common.models import BaseModel
# Create your models here.

class TaskTimer(BaseModel):
    project = models.ForeignKey("time_tracker.Project", on_delete=models.CASCADE)
    task = models.ForeignKey("time_tracker.Task", on_delete=models.CASCADE)
    user = models.ForeignKey("user.User", on_delete=models.SET_NULL, null=True, blank=True)

    name = models.CharField(null=True, blank=True, max_length=100)
    note = models.CharField(null=True, blank=True, max_length=500)

    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)

    class Meta:
        ordering = ['-start_time']


    @property
    def duration_str(self):
        total_seconds = self.duration.total_seconds()
        # convert total_seconds to hours, minutes, seconds
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        seconds = int(total_seconds % 60)
        # format hours minutes  and seconds to 00:00:00
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"