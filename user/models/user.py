from django.db import models
# from common.models import BaseModel
from django.contrib.auth.models import AbstractUser
import uuid

# Create your models here.
class User(AbstractUser):
    id = models.UUIDField(
        primary_key = True,
        default = uuid.uuid4,
        help_text = "Unique ID for this particular object across whole database",
        unique = True
    )

    def __str__(self):
        return self.username
