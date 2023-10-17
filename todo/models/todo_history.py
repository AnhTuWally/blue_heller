from django.db import models
from common.models import BaseModel

from . import Todo
from time_tracker.models import Task, Project

import json

class TodoHistory(BaseModel):
    todo = models.ForeignKey("todo.Todo", on_delete=models.CASCADE)
    # TODO: implement which user modified the field
    # user = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True, blank=True)
    # The field that was modified
    modified_field = models.CharField(max_length=100)
    # The time the field was modified
    timestamp = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    old_value = models.CharField(max_length=100, null=True, blank=True)
    new_value = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.timestamp} | {self.todo.name}.{self.modified_field} | {self.old_value} -> {self.new_value}"
    

    def _serialize_value(self, value):
        serialized_value = None
        if isinstance(value, models.Model):
            serialized_value = value.id
        else:
            serialized_value = str(value)
        
        if serialized_value is None:
            raise Exception(f"Could not serialize value {value}.")
        
        return json.dump({"type": type(value).__name__,
                          "value": serialized_value})

    def set_new_value(self, new_value):
        self.new_value = self._serialize_value(new_value) 
    

    def set_old_value(self, old_value):
        self.old_value = self._serialize_value(old_value)
    

    def _deserialize_value(self, serialized_value):

        serialized_value = json.loads(serialized_value)

        value_type = serialized_value.get("type", None)
        value = serialized_value.get("value", None)

        if value_type is None or value is None:
            raise RuntimeError(f"Could not deserialize value {serialized_value}.")

        if value_type == "str":
            return value

        if value_type == "int":
            return int(value)

        if value_type == "float":
            return float(value)

        if value_type == "bool":
            return bool(value)

        if value_type == Task.__name__:
            return Task.objects.get(id=value)
        
        if value_type == Project.__name__:
            return Project.objects.get(id=value)
        
        if value_type == Todo.__name__:
            return Todo.objects.get(id=value)
        
        raise ValueError(f"Deserialize type {value_type} of {serialized_value} is not implemented.")
        
    
    

