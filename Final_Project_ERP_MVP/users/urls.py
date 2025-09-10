from django.contrib.auth.views import LoginView
from django.urls import path

from .views import (
    MyLogoutView,
    RegisterView,
    UserDeleteView,
    UserDetailView,
    UserProfileUpdateView,
)

lgn = 'users/login.html'

urlpatterns = [
    path('register/', RegisterView.as_view(),
         name='register'),
    path('login/', LoginView.as_view(template_name=lgn),
         name='login'),
    path('logout/', MyLogoutView.as_view(),
         name='logout'),
    path('profile/', UserDetailView.as_view(),
         name='user_detail'),
    path('profile/edit/', UserProfileUpdateView.as_view(),
         name='user_profile_edit'),
    path('profile/delete/', UserDeleteView.as_view(),
         name='user_delete'),
]
