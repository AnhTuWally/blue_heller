from django.db import models
from common.models import BaseModel
from django.core.validators import MinValueValidator, MaxValueValidator

class Todo(BaseModel):
    """A todo is a smaller unit of work that is part of a task.

    It has a priority and urgency.
    It also has a status of done or not done, which is in the form of a checkbox.

    Urgency and priority are used to calculate the Eisenhower Matrix. 

                    | Urgent            | Not Urgent                |
    Important       | Do it Now         | Schedule a time to do it  |
    Not Important   | Delegate          | Eliminate                 |

    TODO: 
        [ ] Add Eisenhower Matrix to UI/webview

    """
    # The name of the todo
    name = models.CharField(max_length=100)
    # The priority of the todo (0-100)
    priority = models.IntegerField(default=0, 
                                   validators=[MinValueValidator(0, message="Priority must be between 0 and 100"),
                                                MaxValueValidator(100, message="Priority must be between 0 and 100")])

    # The urgency of the todo (0-5)
    urgency = models.IntegerField(default=0,
                                    validators=[MinValueValidator(0, message="Urgency must be between 0 and 5"),
                                                MaxValueValidator(5, message="Urgency must be between 0 and 5")])
    is_done = models.BooleanField(default=False)
    task = models.ForeignKey("time_tracker.Task", on_delete=models.SET_NULL, null=True, blank=True)
    project = models.ForeignKey("time_tracker.Project", on_delete=models.SET_NULL, null=True, blank=True)
    linked_to = models.ForeignKey("time_tracker.Todo", on_delete=models.SET_NULL, null=True, blank=True)


    def __str__(self):
        return self.name 