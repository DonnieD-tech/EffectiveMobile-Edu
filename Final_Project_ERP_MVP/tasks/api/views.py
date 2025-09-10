from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied

from tasks.api.permissions import IsAssigneeOrManager
from tasks.api.serializers import (
    TaskCommentCreateSerializer,
    TaskCommentSerializer,
    TaskCreateUpdateSerializer,
    TaskSerializer,
)
from tasks.models import Task, TaskComment


class TaskListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return TaskCreateUpdateSerializer
        return TaskSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == user.Role.MANAGER:
            return Task.objects.filter(
                team__in=user.admin_teams.all()
            )
        return Task.objects.filter(
            team__in=user.admin_teams.all(),
            assignee=user
        )

    def perform_create(self, serializer):
        if self.request.user.role != self.request.user.Role.MANAGER:
            raise PermissionDenied(
                "Создавать задачи может только менеджер"
            )
        serializer.save(created_by=self.request.user)


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return TaskCreateUpdateSerializer
        return TaskSerializer

    def get_queryset(self):
        return Task.objects.filter(
            team__in=self.request.user.admin_teams.all()
        )

    def perform_update(self, serializer):
        if self.request.user.role != self.request.user.Role.MANAGER:
            raise PermissionDenied(
                "Редактировать задачи может только менеджер"
            )
        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user.role != self.request.user.Role.MANAGER:
            raise PermissionDenied(
                "Удалять задачи может только менеджер"
            )
        instance.delete()


class TaskCommentListCreateView(generics.ListCreateAPIView):
    def get_permissions(self):
        return [permissions.IsAuthenticated()]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return TaskCommentCreateSerializer
        return TaskCommentSerializer

    def get_queryset(self):
        task_id = self.kwargs["task_id"]
        return TaskComment.objects.filter(task_id=task_id)

    def perform_create(self, serializer):
        task = get_object_or_404(Task,
                                 pk=self.kwargs["task_id"]
                                 )
        user = self.request.user
        if (user != task.assignee
                and user.role != user.Role.MANAGER):
            raise PermissionDenied(
                "Комментировать могут только"
                " менеджер или исполнитель"
            )
        serializer.save(author=user, task=task)


class TaskCommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskCommentSerializer
    permission_classes = [IsAssigneeOrManager]

    def get_queryset(self):
        return TaskComment.objects.filter(
            task_id=self.kwargs["task_id"]
        )
