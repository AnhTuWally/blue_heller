from django.db import models
from common.models import BaseModel

from datetime import timedelta
# Create your models here.

class Task(BaseModel):
    project = models.ForeignKey("time_tracker.Project", on_delete=models.CASCADE)

    name = models.CharField(null=True, blank=True, max_length=100)
    description = models.CharField(null=True, blank=True, max_length=500)

    @property
    def total_time(self):
        total = timedelta()
        for task_timer in self.tasktimer_set.all():
            if task_timer.duration:
                total +=task_timer.duration
            
        return total
    
    @property
    def total_time_str(self):
        total_seconds = self.total_time.total_seconds()
        # convert total_seconds to hours, minutes, seconds
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        seconds = int(total_seconds % 60)
        # format hours minutes  and seconds to 00:00:00
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

