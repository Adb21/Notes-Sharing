from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["username", "first_name", "last_name", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}, "email": {"required": True}}

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data)


class UserLoginSerializer(TokenObtainPairSerializer):
    """Get user login details serializer"""

    def validate(self, attrs):
        # Default response contains - access token and refresh token
        data = super(UserLoginSerializer, self).validate(attrs)

        # Add custom data for response
        data.update(
            {
                "id": self.user.id,
                "email": self.user.email,
                "username": self.user.username,
            }
        )

        return data
