from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from accounts.views import UserLoginView, UserRegistrationView

urlpatterns = [
    path("signup", UserRegistrationView.as_view(), name="user-registration"),
    path("login", UserLoginView.as_view(), name="login-api"),
    path("login/refresh", TokenRefreshView.as_view(), name="refresh-token-api"),
]
