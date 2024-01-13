from django.contrib.auth import get_user_model
from rest_framework import serializers

from operations.models import Notes

User = get_user_model()


class NoteSerializer(serializers.ModelSerializer):
    """Note CRUD Operation Serializer"""

    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    created_by = serializers.CharField(source="created_by.username", read_only=True)

    class Meta:
        model = Notes
        exclude = ("shareble_id", "expiry_at")

    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        return super().create(validated_data)
