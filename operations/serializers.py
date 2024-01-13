from django.contrib.auth import get_user_model
from rest_framework import serializers

from operations.models import Notes

User = get_user_model()


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notes
        exclude = ("created_by", "shareble_id", "expiry_at")

    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        return super().create(validated_data)
