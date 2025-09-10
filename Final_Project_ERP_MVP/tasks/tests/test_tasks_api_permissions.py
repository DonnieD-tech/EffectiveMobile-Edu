import pytest
from django.utils import timezone
from rest_framework.test import APIRequestFactory

from tasks.api.permissions import IsAssigneeOrManager, IsManager
from tasks.models import Task, TaskComment
from teams.models import Team
from users.models import User


@pytest.mark.django_db
class TestPermissions:
    def test_is_manager_permission(self):
        permission = IsManager()
        factory = APIRequestFactory()

        manager_usr = User.objects.create_user(
            email="manager@list.ru",
            role=User.Role.MANAGER
        )

        regular_usr = User.objects.create_user(
            email="user@list.ru",
            role=User.Role.USER
        )

        request = factory.get("/fake-url/")
        request.user = User()
        assert not permission.has_permission(request, None)

        request.user = regular_usr
        assert not permission.has_permission(request, None)

        request.user = manager_usr
        assert permission.has_permission(request, None)

    def test_is_assignee_or_manager_permission(self):
        permission = IsAssigneeOrManager()
        factory = APIRequestFactory()

        manager_usr = User.objects.create_user(
            email="manager@list.ru",
            role=User.Role.MANAGER
        )
        author_user = User.objects.create_user(
            email="author@list.ru",
            role=User.Role.USER
        )
        assignee_user = User.objects.create_user(
            email="assignee@list.ru",
            role=User.Role.USER
        )
        other_user = User.objects.create_user(
            email="other_user@list.ru",
            role=User.Role.USER
        )
        team = Team.objects.create(
            name="Test Team",
            admin=author_user
        )

        task = Task.objects.create(
            title="Test Task",
            created_by=author_user,
            assignee=assignee_user,
            deadline=timezone.now(),
            team=team
        )

        comment = TaskComment.objects.create(
            author=author_user,
            task=task,
            content="Test comment"
        )

        request = factory.get("/fake-url/")

        request.user = author_user
        assert permission.has_object_permission(request, None, comment)

        request.user = assignee_user
        assert permission.has_object_permission(request, None, comment)

        request.user = manager_usr
        assert permission.has_object_permission(request, None, comment)

        request.user = other_user
        assert not permission.has_object_permission(request, None, comment)
