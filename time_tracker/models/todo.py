from django.db import models
from common.models import BaseModel
from django.core.validators import MinValueValidator, MaxValueValidator

class Todo(BaseModel):
    name = models.CharField(max_length=100)
    priority = models.IntegerField(default=0, 
                                   validators=[MinValueValidator(0, message="Priority must be between 0 and 100"),
                                                MaxValueValidator(100, message="Priority must be between 0 and 100")])
    urgency = models.IntegerField(default=0,
                                    validators=[MinValueValidator(0, message="Urgency must be between 0 and 5"),
                                                MaxValueValidator(5, message="Urgency must be between 0 and 5")])
    is_done = models.BooleanField(default=False)
    task = models.ForeignKey("time_tracker.Task", on_delete=models.SET_NULL, null=True, blank=True)
    project = models.ForeignKey("time_tracker.Project", on_delete=models.SET_NULL, null=True, blank=True)
    linked_to = models.ForeignKey("time_tracker.Todo", on_delete=models.SET_NULL, null=True, blank=True)


    def __str__(self):
        return self.name 