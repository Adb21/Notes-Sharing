from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

# Create your models here.


class Notes(models.Model):
    """Note Model"""

    title = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    shareble_id = models.UUIDField(null=True, blank=True)
    expiry_at = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return self.title


class NoteContents(models.Model):
    """Note Contents Model"""

    note = models.ForeignKey(Notes, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self) -> str:
        return self.note.title
