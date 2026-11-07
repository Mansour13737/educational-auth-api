from django.urls import path
from rest_framework_simplejwt.views import (
    TokenBlacklistView,
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import ChangePasswordView, ProfileView, RegisterView

urlpatterns = [
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/login/", TokenObtainPairView.as_view(), name="login"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/change-password/", ChangePasswordView.as_view(), name="change_password"),
    path("auth/logout/", TokenBlacklistView.as_view(), name="logout"),
    path("profile/", ProfileView.as_view(), name="profile"),
]