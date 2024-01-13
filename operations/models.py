import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

User = get_user_model()

# Create your models here.


class Notes(models.Model):
    """Note Model"""

    title = models.CharField(max_length=255)
    content = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    shareble_id = models.UUIDField(null=True, blank=True)
    expiry_at = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return self.title

    @classmethod
    def generate_sharable_id(cls, instance):
        current_time = timezone.now()
        if instance.shareble_id and current_time < instance.expiry_at:
            return instance.shareble_id
        instance.shareble_id = uuid.uuid4()
        instance.expiry_at = current_time + timezone.timedelta(hours=4)
        instance.save()
        return instance.shareble_id
