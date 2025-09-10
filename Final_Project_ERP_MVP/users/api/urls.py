from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from users.api.views import (
    CurrentUserView,
    UserDetailView,
    UserListView,
    UserRegisterView,
)

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(),
         name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(),
         name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(),
         name="token_verify"),

    path("users/register/", UserRegisterView.as_view(),
         name="user_register"),
    path("users/me/", CurrentUserView.as_view(),
         name="user_me"),
    path("users/", UserListView.as_view(),
         name="user_list"),
    path("users/<int:pk>/", UserDetailView.as_view(),
         name="user_detail"),
]
