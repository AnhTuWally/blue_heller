from django.db import models
from common.models import BaseModel

# Create your models here.
class StickyNote(BaseModel):
    """
    Sticky Note Model

    Attributes:
        user (ForeignKey): User who created the note 
        project (ForeignKey): Project the note is associated with
        name (CharField): Name of the note
        note (CharField): Note content, created by Quill -> in html format
        status (ForeignKey): Status of the note
    """

    user = models.ForeignKey("user.User", on_delete=models.CASCADE)
    project = models.ForeignKey("time_tracker.Project", on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(null=True, blank=True, max_length=100)
    note = models.CharField(null=True, blank=True, max_length=500)
    status = models.ForeignKey('status.NoteStatus', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['-time_created']

    def __str__(self):
        return f"<StickyNote: name={self.name}, user={self.user}, project={self.project}>"
        
