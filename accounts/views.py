from rest_framework import generics
from rest_framework_simplejwt.views import TokenObtainPairView

from accounts.serializers import UserLoginSerializer, UserRegistrationSerializer


class UserRegistrationView(generics.CreateAPIView):
    """User Registration View"""

    serializer_class = UserRegistrationSerializer


class UserLoginView(TokenObtainPairView):
    """Get user login information with access and refresh token view"""

    serializer_class = UserLoginSerializer
