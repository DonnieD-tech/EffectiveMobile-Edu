from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated

from users.api.serializers import (
    UserRegisterSerializer,
    UserSerializer,
    UserUpdateSerializer,
)
from users.models import User


class UserRegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]


class CurrentUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role in [User.Role.MANAGER,
                         User.Role.ADMIN_TEAM]:
            return User.objects.all()
        return User.objects.filter(id=user.id)


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role in [User.Role.MANAGER,
                         User.Role.ADMIN_TEAM]:
            return User.objects.all()
        return User.objects.filter(id=user.id)
