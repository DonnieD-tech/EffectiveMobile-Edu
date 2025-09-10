from rest_framework import permissions

from users.models import User


class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.role == User.Role.MANAGER
                )


class IsAssigneeOrManager(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.user == obj.author
            or request.user == obj.task.assignee
            or request.user.role == User.Role.MANAGER
        )
